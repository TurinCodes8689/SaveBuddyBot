import os
import streamlit as st
import streamlit.components.v1 as components
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.messages.utils import convert_to_messages
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(model="llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful Finance-based AI Assistant who answers questions regarding finance and nothing else, and you will be working for SaveBuddy.")]

st.set_page_config(page_title="SaveBuddy Bot", layout="centered")

st.markdown(
    """
    <style>
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
        background-color: #f0f0f0;
        padding: 20px;
    }
    .chat-container {
        background-color: #F9FAFB;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 800px;
        height: 500px;
        overflow-y: auto;
    }
    .message-box {
        background-color: #ffffff;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        max-width: 75%;
    }
    .human-message {
        background-color: #D1E7FF;
        align-self: flex-start;
        color : black;
    }
    .ai-message {
        background-color: #F0F8FF;
        align-self: flex-end;
        color : black;
    }
    .input-box {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .go-to-app {
        text-align: center;
        margin-top: 20px;
    }
    .go-to-app button {
        background-color: #FF5733;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .go-to-app button:hover {
        background-color: #E04E2A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SaveBuddy Bot")
st.write("Chat with the SaveBuddy Assistant")

chat_container = st.container()

with chat_container:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            st.markdown(f'<div class="message-box human-message">{message.content}</div>', unsafe_allow_html=True)
        elif isinstance(message, AIMessage):
            st.markdown(f'<div class="message-box ai-message">{message.content}</div>', unsafe_allow_html=True)

with st.form(key="chat_form"):
    query = st.text_input("You:", "")
    submit_button = st.form_submit_button(label="Send Message")

if submit_button and query:
    human_message = HumanMessage(content=query)
    st.session_state.chat_history.append(human_message)
    converted_messages = convert_to_messages(st.session_state.chat_history)
    result = model.invoke(converted_messages)
    response = result.content
    ai_message = AIMessage(content=response)
    st.session_state.chat_history.append(ai_message)
    st.rerun()

reset_button = st.button("Reset Conversation", key="reset_button")
if reset_button:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful Finance-based AI Assistant who answers questions regarding finance and nothing else, and you will be working for SaveBuddy.")]
    st.rerun()

st.markdown(
    '<div class="go-to-app"><a href="https://savebuddylives.vercel.app/" target="_self"><button>Go To Main App</button></a></div>',
    unsafe_allow_html=True
)
