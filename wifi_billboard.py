#!/usr/bin/python3

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import starlette.status as status
from fastapi.staticfiles import StaticFiles
from typing import Optional
import subprocess
from config import DEV_ID, PHY_ADDR, LOGIC_ADDR, AI_CHAT_BIO
import os
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from enum import Enum


class ChatState(Enum):
    LOGIN = 0
    CHECK_ASK = 1
    ASK = 2
    WAIT = 3
    GET = 4
    FINISH = 5


temp_dir = tempfile.gettempdir()
app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

BILLBOARD_TEMPLATE = os.path.join("templates", "billboard.html")
BILLBOARD_OUT = os.path.join(temp_dir, "wifi_billboard.html")
CHROME_DATA_DIR = os.path.join(temp_dir, "wifi_bb_chrome_profile")
MAX_TIMEOUT = 20
app.chrome_instance = None  # For displaying custom message
app.browser = None  # For AI chat


def init_ai_chat():
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--enable-javascript')
    options.add_argument('--start-maximized')

    app.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    app.browser.implicitly_wait(2)
    app.browser.get("https://pi.ai/talk")


def click_button():
    try:
        print("DBG Submitting.")
        wait = WebDriverWait(app.browser, 4)
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()
        return True
    except Exception as e:
        print("CLICK ERR:", e)
        return False


def find_text_input_box():
    print("DBG Looking for textarea.")
    textarea = app.browser.find_elements(By.TAG_NAME, "textarea")
    if textarea:
        return True
    else:
        return False


def ask_ai_question(question):
    try:
        input_box = app.browser.find_element(By.TAG_NAME, "textarea")
        print("DBG Populating text area.")
        input_box.clear()
        input_box.send_keys(question)

        return click_button()
    except Exception as e:
        print("ASK ERR:", e)

    return False


def ask_ai(question):
    state = ChatState.CHECK_ASK
    start_time = time.time()
    timeout_reached = False

    if app.chrome_instance:
        app.chrome_instance.terminate()
    if app.browser:
        app.browser.maximize_window()
    else:
        init_ai_chat()

    while state != ChatState.FINISH and not timeout_reached:
        print("\tDBG STATE:", state)

        if state == ChatState.CHECK_ASK:
            if find_text_input_box():
                state = ChatState.ASK
            else:
                state = ChatState.LOGIN

        elif state == ChatState.LOGIN:
            if click_button():
                state = ChatState.CHECK_ASK
            else:
                state = ChatState.FINISH

        elif state == ChatState.ASK:
            if ask_ai_question(question):
                state = ChatState.FINISH

        timeout_reached = (time.time() - start_time) > MAX_TIMEOUT

    if timeout_reached:
        print("ERR: Timeout reached")

    return not timeout_reached


def create_html(message):
    try:
        bb_file = open(BILLBOARD_TEMPLATE, "r")
        data = bb_file.read()
        bb_file.close()

        data = data.replace("{{message}}", message)

        bb_out_file = open(BILLBOARD_OUT, "w")
        bb_out_file.write(data)
        bb_out_file.close()

        return BILLBOARD_OUT
    except Exception as e:
        print(f"ERROR: Could not create the billboard file: {e}")

    return None


def close_billboard():
    if app.chrome_instance:
        app.chrome_instance.terminate()
    if app.browser:
        app.browser.minimize_window()


def send_to_monitor(message):
    close_billboard()

    if create_html(message):
        # Grab HDMI focus
        subprocess.run(["cec-ctl", f"-d{DEV_ID}", f"-t{LOGIC_ADDR}", "--active-source", f"phys-addr={PHY_ADDR}"])
        external_app_params = ["/usr/bin/google-chrome-stable", BILLBOARD_OUT, "--new-window", f"--user-data-dir={CHROME_DATA_DIR}", "--start-maximized"]
        app.chrome_instance = subprocess.Popen(external_app_params)


@app.on_event("startup")
async def startup_event():
    init_ai_chat()
    ask_ai(AI_CHAT_BIO)
    app.browser.minimize_window()


@app.get("/")
def index(request: Request, question: str = "", message: str = "", error: str = ""):
    return templates.TemplateResponse(
        'index.html',
        context={
            'request': request,
            'question': question,
            'message': message,
            'error': error
        }
    )


@app.post("/question")
def ask_question(message: Optional[str] = Form("")):
    if ask_ai(message):
        error = ""
    else:
        error = "No response from AI"

    return RedirectResponse(f"/?question={message}&error={error}", status_code=status.HTTP_302_FOUND)


@app.post("/message")
def post_message(message: Optional[str] = Form("")):
    send_to_monitor(message)
    return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)


@app.get("/api/{command}")
def api_message(command, message: str = ""):
    if command == "send":
        send_to_monitor(message)
        return f"OK, M: {message}"

    elif command == "ask":
        if ask_ai(message):
            return f"OK, Check monitor."
        else:
            return f"ERROR: No response"

    elif command == "close":
        close_billboard()
        return "OK"
    else:
        return f"ERROR, unknown command: {command}"
