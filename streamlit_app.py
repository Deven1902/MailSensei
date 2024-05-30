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
    return gmail_client if await gmail_client.connect() else None

def login_form():
    st.header("User Login")
    st.write("Please enter your email ID and Gmail app password to proceed.")
    email = st.text_input("Email ID", key="email", value=st.session_state.get("email", ""))
    password = st.text_input("App Password", type="password", key="password", value=st.session_state.get("password", ""))
    return email, password

async def initialize_models_with_spinner():
    with st.spinner('Initializing models...'):
        await initialize_models()
    st.success("Models initialized successfully")
    st.session_state.models_initialized = True

async def initialize_app():
    state_defaults = {
        "models_initialized": False,
        "show_form": True,
        "gmail_client": None,
        "clicked_connect": False,
        "page": 1,
        "emails_per_page": 10
    }
    for key, value in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

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
                    await initialize_models_with_spinner()
                else:
                    st.session_state.show_form = True
                    st.error("Failed to connect to Gmail. Please check your credentials and try again.")
            else:
                st.error("Please enter your email ID and password to proceed.")
    else:
        if not st.session_state.models_initialized:
            await initialize_models_with_spinner()

    return st.session_state.gmail_client and st.session_state.models_initialized and not st.session_state.show_form

async def get_emails():
    gmail_client = st.session_state.gmail_client
    page = st.session_state.page
    emails_per_page = st.session_state.emails_per_page
    start_idx = (page - 1) * emails_per_page
    end_idx = start_idx + emails_per_page
    
    if gmail_client:
        with st.spinner('Fetching emails...'):
            unread_email_ids = await gmail_client.fetch_unread_email_ids()
            if unread_email_ids:
                tasks = [gmail_client.fetch_email(email_id) for email_id in unread_email_ids[start_idx:end_idx]]
                fetched_emails = await asyncio.gather(*tasks)
                st.success("Fetched emails successfully")
                return fetched_emails, len(unread_email_ids)
            else:
                st.warning("No unread emails found")
                return None, 0
    else:
        if st.session_state.clicked_connect:
            st.error("Error connecting to Gmail. Please check your credentials and try again.")
        return None, 0

async def render_email(email):
    email_content = strip_tags(email['Content'])
    summary, tags, spam = await asyncio.gather(
        summarize_text(email_content),
        get_tags(email_content),
        detect_spam(email_content)
    )
    
    with st.expander("Email Details", expanded=True):
        st.write(f"From: {email['Sender']}")
        st.write(f"Subject: {email['Subject']}")
        st.write(f"Content: {email_content}")
        st.write(f"Summary: {summary}")
        st.write(f"Tags: {tags}")
        st.write(f"Spam: {spam}")

async def main():
    configure_page()
    content_placeholder = st.empty()
    
    # Initialize the app
    with content_placeholder.container():
        placeholder = st.empty()
        app_initialized = await initialize_app()
        if not app_initialized:
            return
        else:
            fetched_emails, total_emails = await get_emails()
            placeholder.empty()

    # Display emails
    with content_placeholder.container():
        if fetched_emails:
            for i, email in enumerate(fetched_emails):
                st.write(f"From: {email['Sender']}")
                st.write(f"Subject: {email['Subject']}")
                if st.button("View", key=i):
                    await render_email(email)
                st.write("-----")
            
            # Pagination controls
            total_pages = (total_emails + st.session_state.emails_per_page - 1) // st.session_state.emails_per_page
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.session_state.page > 1:
                    if st.button("Previous page"):
                        st.session_state.page -= 1
                        st.experimental_rerun()
            with col2:
                st.write(f"Page {st.session_state.page} of {total_pages}")
            with col3:
                if st.session_state.page < total_pages:
                    if st.button("Next page"):
                        st.session_state.page += 1
                        st.experimental_rerun()

if __name__ == "__main__":
    asyncio.run(main())
