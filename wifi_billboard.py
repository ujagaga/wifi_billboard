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

CLEARANCE = "\n" * 40


def send_to_monitor(message):
    # Grab HDMI focus
    subprocess.run(["cec-ctl", f"-d{DEV_ID}", f"-t{LOGIC_ADDR}", "--active-source", f"phys-addr={PHY_ADDR}"])
    # Write message to console
    subprocess.run(['sudo', '/bin/bash', '/tmp/write_tty', message])


@app.on_event("startup")
async def startup_event():
    # Create a shell script to use to output data to tty0
    out_text = f'echo "$1" > /dev/{HDMI_CONSOLE}'
    print(f'Preparing write out file "/tmp/write_tty" with: \n{out_text}')
    with open("/tmp/write_tty", "w") as out_file:
        out_file.write(out_text)


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
    send_to_monitor(CLEARANCE)
    send_to_monitor(message)
    return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)


@app.get("/api/{command}")
def api_message(command, message: str = ""):
    if command == "send":
        send_to_monitor(message)
        return f"OK, M: {message}"
    elif command == "ask":
        send_to_monitor(message)
        return f"OK, M: {message}"
    elif command == "clear":
        send_to_monitor(CLEARANCE)
        return "OK"
    else:
        return f"ERROR, unknown command: {command}"
