def chatbot(user_query: str):
    import configparser
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.chat_history import (
    BaseChatMessageHistory, 
    InMemoryChatMessageHistory
    )
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from operator import itemgetter
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.messages import SystemMessage, trim_messages, AIMessage, HumanMessage


    config = configparser.ConfigParser()
    config.read('../creds.cfg')
    os.environ["OPENAI_API_KEY"]=config["OPENAI"]["OPENAI_API_KEY"]
    os.environ["OPENAI_API_ENDPOINT"]=config["OPENAI"]["OPENAI_API_ENDPOINT"]



    model = ChatOpenAI(model="gpt-3.5-turbo")



    store = {}

    def get_session_history(session_id: str)->BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    with_message_history = RunnableWithMessageHistory(model, get_session_history)



    trimmer = trim_messages(
        max_tokens = 65,
        strategy = "last",
        token_counter = model, 
        include_system = True, 
        allow_partial=False, 
        start_on="human"
        )
   
    messages = []

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all question to the best of your ability in {language}."
            ),
            MessagesPlaceholder(variable_name="messages")
            
        ]
    )

    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | prompt | model
    )

    with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")
    config = {"configurable": {"session_id":"abc21"}}

    response = with_message_history.invoke({"messages": messages + [HumanMessage(content=user_query)], "language":"English"}, config=config)
    chatbot_response = response.content

    return chatbot_response
