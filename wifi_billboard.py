#!/usr/bin/python3

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import starlette.status as status
from fastapi.staticfiles import StaticFiles
from typing import Optional
import subprocess

# sudo cec-ctl --list-devices
# sudo cec-ctl -d/dev/cec0 --playback -S
# cec-ctl -d/dev/cec0 --to 0 --active-source phys-addr=1.0.0.0
# Writing to screen: echo "foo" > /dev/tty0


TV_ADDR = "1.0.0.0"

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")


def send_to_monitor(message, endpoint="/dev/tty0"):
    with open(endpoint, "a") as display:
        display.write(message)


def grab_hdmi_focus():
    subprocess.run(["cec-ctl", "-d/dev/cec0", "--t0", "--active-source", f"phys-addr={TV_ADDR}"])


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