#!/usr/bin/python3

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import starlette.status as status
from fastapi.staticfiles import StaticFiles
from typing import Optional


app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")


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