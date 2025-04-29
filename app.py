import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Streamlit UI
st.title("💬 Open-Source LLM Chat with Groq")
st.caption("🚀 A Streamlit chatbot powered by Groq's fast LLMs")

# Model selection
model = st.sidebar.selectbox(
    "Choose a model",
    ["llama3-8b-8192", "llama3-70b-8192", "llama-3.3-70b-versatile", "gemma2-9b-it"] #Working models as on 26-04-25
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream the response from Groq
        for response in client.chat.completions.create(
                model=model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})