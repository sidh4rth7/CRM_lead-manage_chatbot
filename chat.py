import streamlit as st
from streamlit_chat import message
from assistant import Assistant
from langchain.callbacks import StreamlitCallbackHandler
 
assistant = Assistant()
assistant.initialize()

st.set_page_config(page_title="🤖CRM - Lead ManageBOT🤖")
st.title("🤖CRM - Lead ManageBOT🤖")

def chatbot_response(prompt):
    return assistant.get_answer(prompt)


prompt = st.chat_input("Say something")
if prompt:
    response = chatbot_response(prompt)
    message(prompt, is_user=True,logo=None,avatar_style=None)
    message(response,logo=None,avatar_style=None)