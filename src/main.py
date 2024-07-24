from typing import Union 
from fastapi import FastAPI, Response, status

from controller import invoke_chatbot
from model import UserPrompt

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.post("/chatbot")
def chatbot(user_prompt: UserPrompt):
    try:
        chatbot_response = invoke_chatbot(user_prompt.prompt)
        return chatbot_response
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)