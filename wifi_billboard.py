#!/usr/bin/python3

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import starlette.status as status
from fastapi.staticfiles import StaticFiles
from typing import Optional
import subprocess
from config import DEV_ID, PHY_ADDR, LOGIC_ADDR, INSTA_USER, INSTA_PASS, INSTA_RECIPIENT, INSTA_TIMEOUT_S
import os
import tempfile
import instagrapi
import json
import time


temp_dir = tempfile.gettempdir()
app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

BILLBOARD_TEMPLATE = os.path.join("templates", "billboard.html")
BILLBOARD_OUT = os.path.join(temp_dir, "wifi_billboard.html")
CHROME_DATA_DIR = os.path.join(temp_dir, "wifi_bb_chrome_profile")

app.chrome_instance = None
app.insta_client = None


def instagram_login_and_get_ai_user():
    global app

    send_to = None
    try:
        if not app.insta_client:
            app.insta_client = instagrapi.Client()
            app.insta_client.login(INSTA_USER, INSTA_PASS)

        send_to = app.insta_client.user_id_from_username(username=INSTA_RECIPIENT)
    except Exception as e:
        print("ERROR:", e)
        app.insta_client.logout()
        app.insta_client = instagrapi.Client()
        app.insta_client.login(INSTA_USER, INSTA_PASS)

        send_to = app.insta_client.user_id_from_username(username=INSTA_RECIPIENT)

    return send_to


def instagram_do_dialog(message):
    try:
        send_to = instagram_login_and_get_ai_user()
        message_details = app.insta_client.direct_send(text=message, user_ids=[send_to])
        print('Sent to instagram:', message_details)
        thread_id = message_details["thread_id"]

        start_time = time.time()
        while time.time() - start_time < INSTA_TIMEOUT_S:
            messages = app.insta_client.direct_messages(thread_id=thread_id, amount=1)
            response = messages[0]
            if not response.is_sent_by_viewer:
                print(f"Response in {int(time.time() - start_time)}s: {response.text}")
                return {"response": response.text, "error": ""}
        return {"response": "", "error": "Instagram query timed out"}

    except Exception as e:
        print("ERROR: Failed to send message:", e)
        return {"response": "", "error": f"{e}"}


def create_html(question, answer):
    try:
        bb_file = open(BILLBOARD_TEMPLATE, "r")
        data = bb_file.read()
        bb_file.close()

        if question:
            question = f"Question: {question}"
        else:
            question = ""

        data = data.replace("{{answer}}", answer).replace("{{question}}", question)

        bb_out_file = open(BILLBOARD_OUT, "w")
        bb_out_file.write(data)
        bb_out_file.close()

        return BILLBOARD_OUT
    except Exception as e:
        print(f"ERROR: Could not create the billboard file: {e}")

    return None


def send_to_monitor(question, answer):
    if create_html(question, answer):
        # Grab HDMI focus
        subprocess.run(["cec-ctl", f"-d{DEV_ID}", f"-t{LOGIC_ADDR}", "--active-source", f"phys-addr={PHY_ADDR}"])
        external_app_params = ["/usr/bin/google-chrome-stable", BILLBOARD_OUT, "--new-window", f"--user-data-dir={CHROME_DATA_DIR}", "--start-maximized"]
        app.chrome_instance = subprocess.Popen(external_app_params)


def close_billboard():
    if app.chrome_instance:
        app.chrome_instance.terminate()


@app.get("/")
def index(request: Request, question: str = "", answer: str = "", message: str = "", error: str = ""):
    return templates.TemplateResponse(
        'index.html',
        context={
            'request': request,
            'question': question,
            'answer': answer,
            'message': message,
            'error': error
        }
    )


@app.post("/question")
def ask_question(message: Optional[str] = Form("")):
    answer = instagram_do_dialog(message)
    if answer['error']:
        send_to_monitor(question=message, answer=f"ERROR: {answer['error']}")
    else:
        send_to_monitor(question=message, answer=answer['response'])

    return RedirectResponse(f"/?question={message}&answer={answer['response']}&error={answer['error']}", status_code=status.HTTP_302_FOUND)


@app.post("/message")
def post_message(message: Optional[str] = Form("")):
    send_to_monitor(question="", answer=message)
    return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)


@app.get("/api/{command}")
def api_message(command, message: str = ""):
    if command == "send":
        send_to_monitor(question="", answer=message)
        return f"OK, M: {message}"
    elif command == "ask":
        answer = instagram_do_dialog(message)
        if answer["error"]:
            send_to_monitor(question=message, answer=f"E: {answer['error']}")
            return f"ERROR: {answer['error']}"

        send_to_monitor(question="", answer=answer['response'])
        return f"OK, A: {answer}"
    elif command == "close":
        close_billboard()
        return "OK"
    else:
        return f"ERROR, unknown command: {command}"
