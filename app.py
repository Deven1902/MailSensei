from typing import Dict
import streamlit as st
import requests
import time

# Define API endpoints
API_BASE_URL = "http://localhost:8000"  # Change to your server URL
API_ENDPOINTS = {
    "setup_gmail_credentials": "/setup_gmail_credentials",
    "connect_gmail": "/connect_gmail",
    "fetch_unread_emails": "/fetch_unread_emails",
    "fetch_email_details": "/fetch_email_details",
    "filter_by_sender": "/filter_by_sender",
    "filter_by_subject": "/filter_by_subject",
    "filter_by_importance": "/filter_by_importance",
    "initialize_models": "/initialize_models",
    "summarize_text": "/summarize_text",
    "get_tags": "/get_tags",
    "detect_spam": "/detect_spam",
}

# Utility Functions
def api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """
    Make a request to the API endpoint.
    """
    url = f"{API_BASE_URL}{API_ENDPOINTS[endpoint]}"
    try:
        if method == "GET":
            response = requests.get(url, params=data)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return {}

def setup_gmail_credentials(gmail_address: str, app_password: str) -> Dict:
    """
    Setup Gmail Credentials.
    """
    data = {"gmail_address": gmail_address, "app_password": app_password}
    return api_request("setup_gmail_credentials", method="POST", data=data)

def connect_gmail(username: str, password: str) -> Dict:
    """
    Connect to Gmail IMAP Server.
    """
    data = {"username": username, "password": password}
    return api_request("connect_gmail", method="POST", data=data)

def fetch_unread_emails() -> Dict:
    """
    Fetch IDs of Unread Emails.
    """
    return api_request("fetch_unread_emails", method="GET")

def fetch_email_details(email_id: int) -> Dict:
    """
    Fetch Details of a Specific Email.
    """
    endpoint = f"fetch_email_details/{email_id}"
    return api_request(endpoint, method="GET")

def summarize_text(text: str) -> Dict:
    """
    Summarize Text.
    """
    data = {"text": text}
    return api_request("summarize_text", method="POST", data=data)

def get_tags(text: str) -> Dict:
    """
    Get Tags for Text.
    """
    data = {"text": text}
    return api_request("get_tags", method="POST", data=data)

def detect_spam(text: str) -> Dict:
    """
    Detect Spam in Text.
    """
    data = {"text": text}
    return api_request("detect_spam", method="POST", data=data)

def initialize_models() -> Dict:
    """
    Initialize AI Models.
    """
    return api_request("initialize_models", method="POST")

# Streamlit App
st.set_page_config(layout="wide")

# Page State
PAGE_STATE = st.session_state.get("page_state", "setup_credentials")

# Page: Setup Gmail Credentials
if PAGE_STATE == "setup_credentials":
    st.header("Setup Gmail Credentials")
    gmail_address = st.text_input("Gmail Address")
    app_password = st.text_input("App Password", type="password")
    if st.button("Setup"):
        with st.spinner("Setting up Gmail credentials..."):
            time.sleep(3)  # Simulating delay for demonstration
            response = setup_gmail_credentials(gmail_address, app_password)
            if response.get("success"):
                st.success("Gmail credentials setup successful")
                st.session_state.page_state = "connect_gmail"
            else:
                st.error("Failed to setup Gmail credentials. Please try again.")

# Page: Connect to Gmail
elif PAGE_STATE == "connect_gmail":
    st.header("Connect to Gmail")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Connect"):
        with st.spinner("Connecting to Gmail..."):
            time.sleep(3)  # Simulating delay for demonstration
            response = connect_gmail(username, password)
            if response.get("success"):
                st.success("Connected to Gmail IMAP server")
                st.session_state.page_state = "fetch_unread_emails"
            else:
                st.error("Failed to connect to Gmail IMAP server. Please check your credentials and try again.")

# Page: Fetch Unread Emails
elif PAGE_STATE == "fetch_unread_emails":
    st.header("Unread Emails")
    with st.spinner("Fetching unread emails..."):
        time.sleep(3)  # Simulating delay for demonstration
        response = fetch_unread_emails()
        if response.get("success"):
            email_ids = response.get("email_ids", [])
            if email_ids:
                st.success("Unread email IDs fetched successfully")
                st.write("Unread Email IDs:", email_ids)
            else:
                st.warning("No unread emails found")
        else:
            st.error("Failed to fetch unread emails. Please try again.")

# Page: Fetch Email Details
elif PAGE_STATE == "fetch_email_details":
    st.header("Fetch Email Details")
    email_id = st.text_input("Email ID")
    if st.button("Fetch Details"):
        with st.spinner("Fetching email details..."):
            response = fetch_email_details(email_id)
            if response.get("success"):
                email_details = response.get("email_details")
                if email_details:
                    st.success("Email details fetched successfully")
                    st.write("Email Details:", email_details)
                else:
                    st.warning("No email details found")
            else:
                st.error("Failed to fetch email details. Please try again.")

# Page: Summarize Text
elif PAGE_STATE == "summarize_text":
    st.header("Summarize Text")
    text = st.text_area("Enter Text")
    if st.button("Summarize"):
        with st.spinner("Summarizing text..."):
            response = summarize_text(text)
            if response.get("success"):
                summary = response.get("result")
                if summary:
                    st.success("Text summarized successfully")
                    st.write("Summary:", summary)
                else:
                    st.warning("No summary generated")
            else:
                st.error("Failed to summarize text. Please try again.")

# Page: Get Tags
elif PAGE_STATE == "get_tags":
    st.header("Get Tags for Text")
    text = st.text_area("Enter Text")
    if st.button("Get Tags"):
        with st.spinner("Getting tags..."):
            response = get_tags(text)
            if response.get("success"):
                tags = response.get("result")
                if tags:
                    st.success("Tags retrieved successfully")
                    st.write("Tags:", tags)
                else:
                    st.warning("No tags retrieved")
            else:
                st.error("Failed to get tags. Please try again.")

# Page: Detect Spam
elif PAGE_STATE == "detect_spam":
    st.header("Detect Spam in Text")
    text = st.text_area("Enter Text")
    if st.button("Detect Spam"):
        with st.spinner("Detecting spam..."):
            response = detect_spam(text)
            if response.get("success"):
                result = response.get("result")
                if result:
                    st.success("Spam detected successfully")
                    st.write("Spam Detection Result:", result)
                else:
                    st.warning("No spam detected")
            else:
                st.error("Failed to detect spam. Please try again.")

# Page: Initialize Models
elif PAGE_STATE == "initialize_models":
    st.header("Initialize AI Models")
    if st.button("Initialize Models"):
        with st.spinner("Initializing models..."):
            response = initialize_models()
            if response.get("success"):
                st.success("Models initialized successfully")
                st.balloons()  # Celebratory animation for success
            else:
                st.error("Failed to initialize models. Please try again.")
