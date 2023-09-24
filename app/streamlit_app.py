import streamlit as st
import requests
import email_utils
import LLM

if "model" not in st.session_state.keys():
    st.session_state["model"] = LLM.init()
model = st.session_state["model"]


def start():
    # Streamlit app
    st.title("Email Viewer")

    # Input fields for email credentials
    from_email = st.text_input("Email Address")
    from_password = st.text_input("Password", type="password")

    if st.button("Set Credentials"):
        if not from_email or not from_password:
            st.error("Please provide both email address and password.")
        else:
            if email_utils.set_credentials(from_email, from_password):
                st.success(
                    f"Credentials set successfully. Email: {from_email}"
                )
                email_ids = email_utils.fetch_emails_from_imap(from_email,
                                                               from_password)
                st.session_state.update(email_ids=email_ids)

            else:
                st.error("Failed to set credentials")

    if st.button("Fetch Emails"):
        # Fetch email data from the FastAPI API
        try:
            with st.spinner('Loading...'):
                render_emails(from_email, from_password)
        except Exception as e:
            print(e)


def render_emails(from_email, from_password, page_size=10):
    """Renders the email messages in a Streamlit application with pagination.

      Args:
        email_messages: A list of email messages.
        page_number: The current page number.
        page_size: The number of emails to display per page.
      """

    page_number = st.session_state.get("page", 1)
    email_ids = st.session_state.email_ids
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size

    email_messages = email_utils.decode_emails(email_ids, start_index, end_index,
                                               from_email, from_password)

    # Render the email messages for the current page.
    for email_message in email_messages:
        content = email_utils.strip_tags(email_message["content"])
        summary = LLM.summarize(content, model[0])
        tags = LLM.get_tags(content, model[2])
        spam = LLM.detect_spam(content, model[1])
        with st.expander(f"**From**:\n{email_message['from']}\n\n**Subject**:\n{email_message['subject']}\n\n**Tags**:\n{tags[0]['generated_text']}\n\n{'***spam***' if spam == 'spam' else ''}"
                         ):
            st.markdown(f"**Summary** {summary[0]['summary_text']}")

    total = len(st.session_state.email_ids)

    # Add buttons to allow the user to navigate between pages.
    if page_number > 1:
        st.button('Previous page',
                  on_click=lambda: (st.session_state.update(page=page_number - 1), render_emails(from_email, from_password)))
    if page_number < total:
        st.button('Next page',
                  on_click=lambda: (st.session_state.update(page=page_number + 1), render_emails(from_email, from_password)))


if __name__ == "__main__":
    start()
