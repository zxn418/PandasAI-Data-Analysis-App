import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

load_dotenv()

# --- Configure PandasAI + LiteLLM (Ollama, local) ---
llm = LiteLLM(model="gpt-4.1-mini", api_key=os.getenv("OPENAI_API_KEY"))
pai.config.set({"llm": llm})

st.set_page_config(page_title="Chat with your CSV")
st.title("Chat with your CSV")


def check_input(uploaded_file) -> tuple[bool, str]:
    if uploaded_file is None:
        return False, "No file uploaded."
    if not uploaded_file.name.lower().endswith(".csv"):
        return False, "Please upload a .csv file."
    return True, ""


def check_message(message: str) -> tuple[bool, str]:
    if not message or not message.strip():
        return False, "Please enter a question."
    if len(message) > 500:
        return False, "Question is too long (max 500 characters)."
    return True, ""

def render_response(response):
    """Show the response in the right widget based on its type."""
    if isinstance(response, (pd.DataFrame, pd.Series)):
        st.dataframe(response, use_container_width=True)
    elif isinstance(response, str) and response.lower().endswith((".png", ".jpg", ".jpeg")) and os.path.exists(response):
        st.image(response)
    else:
        st.markdown(str(response))

if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    valid, error = check_input(uploaded_file)
    if not valid:
        st.error(error)
    else:
        if st.session_state.get("uploaded_name") != uploaded_file.name:
            st.session_state.df = pai.read_csv(uploaded_file)
            st.session_state.uploaded_name = uploaded_file.name
            st.session_state.messages = []
        st.dataframe(st.session_state.df.head())

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask something about your data...")

if question:
    if st.session_state.df is None:
        st.warning("Upload a CSV first.")
    else:
        ok, error = check_message(question)
        if not ok:
            st.warning(error)
        else:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.df.chat(question)
                    st.markdown(str(response))
            st.session_state.messages.append({"role": "assistant", "content": str(response)})