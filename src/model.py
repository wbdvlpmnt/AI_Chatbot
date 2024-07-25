from pydantic import BaseModel


class Message(BaseModel):
    messageContent:str
    messageType: str