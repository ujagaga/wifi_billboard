#!/usr/bin/python3

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import starlette.status as status
from fastapi.staticfiles import StaticFiles
from typing import Optional
import subprocess
from config import DEV_ID, PHY_ADDR, LOGIC_ADDR, HDMI_CONSOLE


app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")


def send_to_monitor(message):
    subprocess.run(['sudo', '/bin/bash', '/tmp/write_tty', message])


def grab_hdmi_focus():
    subprocess.run(["cec-ctl", f"-d{DEV_ID}", f"-t{LOGIC_ADDR}", "--active-source", f"phys-addr={PHY_ADDR}"])


@app.on_event("startup")
async def startup_event():
    # Create a shell script to use to output data to tty0
    out_text = f'echo "$1" > /dev/{HDMI_CONSOLE}'
    print("Preparing write out file with: ", out_text)
    with open("/tmp/write_tty", "w") as out_file:
        out_file.write()


@app.get("/")
def index(request: Request, question: str = "", answer: str = "", message: str = ""):
    return templates.TemplateResponse(
        'index.html',
        context={
            'request': request,
            'question': question,
            'answer': answer,
            'message': message
        }
    )


@app.post("/question")
def ask_question(question: Optional[str] = Form("")):
    print("Q:", question)
    return RedirectResponse(f"/?question={question}&answer=custom_answer", status_code=status.HTTP_302_FOUND)


@app.post("/message")
def post_message(message: Optional[str] = Form("")):
    print("M:", message)
    return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)