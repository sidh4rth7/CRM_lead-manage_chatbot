from assistant import Assistant
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
 
assistant = Assistant()
assistant.initialize()
#print(assistant.get_answer("Interact with the user till he opts to quit/exit"))

# Simple chatbot function
# def chatbot_response(input_text):
#     return assistant.get_answer(input_text)

# def main():
st.title("Chatbot Demo")

st.sidebar.header("User Input")
user_input = st.sidebar.text_input("Enter your message:")

if st.sidebar.button("Send"):
    if user_input:
        response = assistant.get_answer(user_input)
        st.text(response)

# if __name__ == "__main__":
#     main()






