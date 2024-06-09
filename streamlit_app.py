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

    base64_logo = load_file_content("./assets/logo_base64.txt")
    html_template = load_file_content("./assets/template.html").replace("{{ base64_image }}", base64_logo)
    st.markdown(html_template, unsafe_allow_html=True)

def load_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()

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

def initialize_session_state(defaults):
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

async def initialize_app():
    state_defaults = {
        "models_initialized": False,
        "show_form": True,
        "gmail_client": None,
        "clicked_connect": False,
        "page": 1,
        "emails_per_page": 10,
        "fetched_emails": None,
        "total_emails": 0
    }
    initialize_session_state(state_defaults)

    if st.session_state.show_form:
        email, password = login_form()
        if st.button('Connect'):
            await handle_login(email, password)
    else:
        if not st.session_state.models_initialized:
            await initialize_models_with_spinner()

    return st.session_state.gmail_client and st.session_state.models_initialized and not st.session_state.show_form

async def handle_login(email, password):
    st.session_state.clicked_connect = True
    if email and password:
        st.session_state.show_form = False
        with st.spinner('Connecting to Gmail...'):
            gmail_client = await connect_gmail_client(email, password)
        if gmail_client:
            st.session_state.gmail_client = gmail_client
            st.success("Connected to Gmail successfully")
            await initialize_models_with_spinner()
        else:
            st.session_state.show_form = True
            st.error("Failed to connect to Gmail. Please check your credentials and try again.")
    else:
        st.error("Please enter your email ID and password to proceed.")

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
                st.session_state.fetched_emails = fetched_emails
                st.session_state.total_emails = len(unread_email_ids)
                st.success("Fetched emails successfully")
                return fetched_emails
            else:
                st.warning("No unread emails found")
                return None
    else:
        if st.session_state.clicked_connect:
            st.error("Error connecting to Gmail. Please check your credentials and try again.")
        return None
    
def get_emails_matching_search(query):
    gmail_client = st.session_state.gmail_client
    emails = st.session_state.fetched_emails
    if gmail_client and emails:
        with st.spinner('Searching emails...'):
            matching_emails = [email for email in emails if query.lower() in email['Content'].lower() or query.lower() in email['Sender'].lower() or query.lower() in email['Subject'].lower()]
            if matching_emails:
                st.success("Found matching emails")
                return matching_emails
            else:
                st.warning("No matching emails found")
                return None
    else:
        return None
    
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
        
def render_pagination_controls(total_pages):
    _, col1, col2, col3, _,= st.columns(5)
    with col1:
        if st.session_state.page > 1:
            if st.button("⬅️", key="prev_page"):
                st.session_state.page -= 1
                st.experimental_rerun()
    with col2:
        st.write(f"Page {st.session_state.page} of {total_pages}")
    with col3:
        if st.session_state.page < total_pages:
            if st.button("➡️", key="next_page"):
                st.session_state.page += 1
                st.experimental_rerun()

async def main():
    configure_page()
    content_placeholder = st.empty()
    
    with content_placeholder.container():
        placeholder = st.empty()
        app_initialized = await initialize_app()
        if not app_initialized:
            return
        else:
            if st.session_state.fetched_emails is None:
                fetched_emails = await get_emails()
            else:
                fetched_emails = st.session_state.fetched_emails
            placeholder.empty()

    with content_placeholder.container():
        
        # st.subheader("Search Emails")
        # search_query = st.text_input("Enter query")
        # if search_query:
        #     fetched_emails = get_emails_matching_search(search_query)
        #     if fetched_emails:
        #         st.session_state.original_emails = st.session_state.fetched_emails
        #         st.session_state.fetched_emails = fetched_emails
        # else:
        #     fetched_emails = st.session_state.fetched_emails
            
        if fetched_emails:
            st.subheader("Emails")
            for i, email in enumerate(fetched_emails):
                st.write(f"From: {email['Sender']}")
                st.write(f"Subject: {email['Subject']}")
                if st.button("View", key=f"view_{i}"):
                    await render_email(email)
                st.write("-----")
            
            total_pages = (st.session_state.total_emails + st.session_state.emails_per_page - 1) // st.session_state.emails_per_page
            render_pagination_controls(total_pages)
        
        # # Clear search button
        # if "original_emails" in st.session_state and st.button("Clear Search"):
        #     st.session_state.fetched_emails = st.session_state.original_emails

if __name__ == "__main__":
    asyncio.run(main())
