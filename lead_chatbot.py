import streamlit as st
from streamlit_chat import message
from assistant import Assistant
from langchain.callbacks import StreamlitCallbackHandler
 
assistant = Assistant()
assistant.initialize()

st.set_page_config(page_title="🤖CRM - Lead ManageBOT🤖")
st.title("🤖CRM - Lead ManageBOT🤖")

def query(prompt):
    return assistant.get_answer(prompt)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

prompt = st.chat_input("Say something", key="input_text")

if prompt:
    st.session_state.past.append(prompt)
    st.session_state.generated.append(query(prompt))

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))