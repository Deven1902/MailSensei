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
   
    
async def main():
    configure_page()
    
    # Initialize the models
    placeholder = st.empty()
    with st.spinner('Initializing models...'):
        await initialize_models()
    placeholder.empty()
    st.success("Models initialized successfully")

if __name__ == "__main__":
    asyncio.run(main())
