import asyncio
import streamlit as st
from src.utils.email_utils import GmailClient, strip_tags
from src.utils.hf_utils import (
    summarize_text,
    get_tags,
    detect_spam,
    initialize_models
)

def configure_page():
    st.set_page_config(
        page_title="MAILSENSEI",
        layout="centered",
        initial_sidebar_state="expanded",
        page_icon="./assets/logo.png"
    )

    with open("./assets/logo_base64.txt", "r") as file:
        base64_logo = file.read()

    with open("./assets/template.html", "r") as file:
        html_template = file.read()
        
    html_template = html_template.replace("{{ base64_image }}", base64_logo)
    st.markdown(html_template, unsafe_allow_html=True)

async def connect_gmail_client(email, password):
    gmail_client = GmailClient(email, password)
    if await gmail_client.connect():
        return gmail_client
    else:
        return None

def login_form():
    st.header("User Login")
    st.write("Please enter your email ID and password to initialize the models.")
    email = st.text_input("Email ID", key="email", value=st.session_state.get("email", ""))
    password = st.text_input("Password", type="password", key="password", value=st.session_state.get("password", ""))
    return email, password

async def initialize_app():
    configure_page()

    if 'gmail_client' not in st.session_state:
        st.session_state.gmail_client = None
        
    email, password = login_form()
    if st.button('Connect'):
        if email and password:
            # Connect to Gmail
            with st.spinner('Connecting to Gmail...'):
                gmail_client = await connect_gmail_client(email, password)
            if gmail_client:
                st.session_state.gmail_client = gmail_client
                st.success("Connected to Gmail successfully")
                # Initialize models
                with st.spinner('Initializing models...'):
                    await initialize_models()
                st.success("Models initialized successfully")
            else:
                st.error("Failed to connect to Gmail. Please check your credentials and try again.")
        else:
            st.error("Please enter your email ID and password to proceed.")
    
    return email, password

async def main():
    email, password = await initialize_app()

if __name__ == "__main__":
    asyncio.run(main())
