from model import Message
from models.chatbot import chatbot


def invoke_chatbot(user_query:str)->Message:
    response = chatbot(user_query)
    message: Message = {
        'messageContent' : response,
        'messageType': 'system'
    }
    return message