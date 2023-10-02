import streamlit as st
import email_utils
import LLM


if "model" not in st.session_state.keys():
    st.session_state["model"] = LLM.init()
model = st.session_state["model"]

if "credentials_set" not in st.session_state.keys():
    st.session_state['credentials_set'] = False


def start():
    with st.sidebar:
        st.markdown("# Email Summarizer")
        st.subheader("Email Credentials")
        from_email = st.text_input("Email Address")
        from_password = st.text_input("App Password", type="password")
        if st.button("Set Credentials"):
            if not from_email or not from_password:
                st.error("Please provide both email address and password.")
            else:
                if email_utils.set_credentials(from_email, from_password):
                    st.session_state['credentials_set'] = True
                    st.success(f"Credentials set successfully. Email: {from_email}")
                    email_ids = email_utils.fetch_emails_from_imap(from_email, from_password)
                    st.session_state.update(email_ids=email_ids)
                else:
                    st.error("Failed to set credentials")

    if st.session_state['credentials_set']:
        if st.button("Fetch Emails"):
            try:
                with st.spinner('Loading...'):
                    render_emails(from_email, from_password)
            except Exception as e:
                print(e)
    else:
        st.button("Fetch Emails", disabled=True)
        st.warning("Please set credentials first", icon="⚠️",)


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

    for email_message in email_messages:

        content = email_utils.strip_tags(email_message["content"])
        summary = LLM.summarize(content, model[0])
        tags = LLM.get_tags(content, model[2])
        # spam = LLM.detect_spam(content, model[1])

        # Add a redirect button that links to the original email
        redirect_url = f'https://mail.google.com/mail/u/0/#search/rfc822msgid%3A{email_message["Message ID"]}'

        EMAIL_FROM= email_message['from']
        EMAIL_SUBJECT = email_message['subject'] if email_message['subject'].strip() else "No Subject"
        EMAIL_TAGS = tags[0]['generated_text']
        EMAIL_SUMMARY = summary[0]['summary_text']

        with st.expander(

            f"**From**:\n{EMAIL_FROM}\n\n**Subject**:\n{EMAIL_SUBJECT}\n\n**Tags**:\n{EMAIL_TAGS}\n\n"
        ):
            # tag_html = ''.join([f'<span style="display: inline-block; background-color: rgba(230, 230, 230, 0.2); padding: 3px 6px; margin-right: 8px; border-radius: 5px;">{tag}</span>' for tag in tags[0]['generated_text'].split(',')])

            st.markdown(f"**Summary**:\n {EMAIL_SUMMARY}")
            st.markdown(f"**[Read full e-mail]({redirect_url})**")

        # Handle the button click event
        # if redirect_button_clicked:
        #     st.write(f"Redirecting to Gmail: {redirect_url}")
        #     st.experimental_rerun()  # Refresh the app to open the link

    total = len(st.session_state.email_ids)

    # Add buttons to allow the user to navigate between pages.
    if page_number > 1:
        st.button('Previous page',
                  on_click=lambda: (st.session_state.update(page=page_number - 1),
                                    render_emails(from_email, from_password)))
    if page_number < total:
        st.button('Next page',
                  on_click=lambda: (st.session_state.update(page=page_number + 1),
                                    render_emails(from_email, from_password)))


if __name__ == "__main__":
    start()
