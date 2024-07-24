from models.chatbot import chatbot


def invoke_chatbot(user_query:str):
    response = chatbot(user_query)
    return response