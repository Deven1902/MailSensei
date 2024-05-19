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
    st.write("Please enter your email ID and Gmail app password to proceed.")
    email = st.text_input(
        "Email ID",
        key="email",
        value=st.session_state.get("email", "")
    )
    password = st.text_input(
        "App Password",
        type="password",
        key="password",
        value=st.session_state.get("password", "")
    )
    return email, password

async def initialize_app():

    if 'models_initialized' not in st.session_state:
        st.session_state.models_initialized = False

    if 'show_form' not in st.session_state:
        st.session_state.show_form = True

    if 'gmail_client' not in st.session_state:
        st.session_state.gmail_client = None
        
    if 'clicked_connect' not in st.session_state:
        st.session_state.clicked_connect = False

    if st.session_state.show_form:
        email, password = login_form()

        if st.button('Connect'):
            st.session_state.clicked_connect = True
            if email and password:
                st.session_state.show_form = False
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
                    st.session_state.models_initialized = True
                else:
                    st.session_state.show_form = True
                    st.error("Failed to connect to Gmail. Please check your credentials and try again.")
            else:
                st.error("Please enter your email ID and password to proceed.")
    else:
        if not st.session_state.models_initialized:
            # Initialize models
            with st.spinner('Initializing models...'):
                await initialize_models()
            st.success("Models initialized successfully")
            st.session_state.models_initialized = True
            
    if st.session_state.gmail_client and st.session_state.models_initialized and not st.session_state.show_form:
        return True
    else:
        return False
            
async def get_emails():
    gmail_client = st.session_state.gmail_client
    start_idx = 0
    end_idx = 10
    if gmail_client:
        # Fetch emails
        with st.spinner('Fetching emails...'):
            unread_email_ids = await gmail_client.fetch_unread_email_ids()
            if unread_email_ids:
                tasks = [gmail_client.fetch_email(email_id) for email_id in unread_email_ids[start_idx:end_idx]]
                fetched_emails = await asyncio.gather(*tasks)
                st.success("Fetched emails successfully")
                return fetched_emails
            else:
                st.warning("No unread emails found")
                return None
    else:
        if st.session_state.clicked_connect:
            st.error("Error connecting to Gmail. Please check your credentials and try again.")
        return None
    
async def render_email(email):
    email_content = strip_tags(email['Content'])
    summary = await summarize_text(email_content)
    tags = await get_tags(email_content)
    spam = await detect_spam(email_content)
    
    with st.expander("Email Details", expanded=True):
        st.write(f"From: {email['Sender']}")
        st.write(f"Subject: {email['Subject']}")
        st.write(f"Content: {email_content}")
        st.write(f"Summary: {summary}")
        st.write(f"Tags: {tags}")
        st.write(f"Spam: {spam}")

async def main():
    
    configure_page()
    content_palceholder = st.empty()
    
    # Initialize the app
    with content_palceholder.container():
        placeholder = st.empty()
        app_initialized = await initialize_app()
        if not app_initialized:
            return
        else:
            # Get emails
            fetched_emails = await get_emails()
            placeholder.empty()

    # Display emails
    with content_palceholder.container(border=True):
        if fetched_emails:
            for i, email in enumerate(fetched_emails):
                st.write(f"From: {email['Sender']}")
                st.write(f"Subject: {email['Subject']}")
                if st.button("View", key=i):
                    await render_email(email)
                st.write("-----")
        

if __name__ == "__main__":
    asyncio.run(main())
