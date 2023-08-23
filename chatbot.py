import streamlit as st
from streamlit_chat import message
from assistant import Assistant
from langchain.callbacks import StreamlitCallbackHandler
from itertools import zip_longest
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
assistant = Assistant()
assistant.initialize()

st.set_page_config(page_title="🤖CRM - Lead ManageBOT🤖")
st.title("🤖CRM - Lead ManageBOT🤖")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store chatbot generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(content="""
                    You are a CRM Lead Managing chatbot but your current functions are restricted to managing lead information through actions such as updating, retrieving, creating, and deleting these details.
                    You are advised to solely focus on the 'lead' table within the database unless explicitly prompted otherwise by the user.
                    All the output from the llm should be sent to human tool.
                    It is important to consistently provide responses to every input from users, sharing the outcome corresponding to their input.""")]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages

# #func to get response for the user input
# def chatbot_response(prompt):
#     return assistant.get_answer(prompt)

# def get_response():
#     if st.session_state.prompt:
#         prompt = st.session_state.prompt
#         response = chatbot_response(prompt)
#         message(prompt)
#         message(response) 

def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = assistant.get_answer(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""

#st.chat_input("Ask Away!",on_submit=assistant.get_response,key="prompt")


# Create a text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit)


if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')


# Add credit
st.markdown("""---Made with 🤖 by [Sid]---""")