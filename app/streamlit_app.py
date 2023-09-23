# import streamlit as st
# import requests

# # Define the FastAPI API URL
# API_URL = "http://localhost:8000"  # Adjust the URL as needed

# # Fetch email data from the FastAPI API
# response = requests.get(API_URL)
# emails = response.json().get("emails", [])

# # Streamlit app
# st.title("Email Viewer")

# for email in emails:
#     st.write(f"From: {email['from']}")
#     st.write(f"Subject: {email['subject']}")
#     st.write(f"Content: {email['content']}")
#     st.write("-" * 50)

# import streamlit as st
# import requests

# # Define the FastAPI API URL
# API_URL = "http://localhost:8000/read-emails"  # Adjust the URL as needed

# # Streamlit app
# st.title("Email Viewer")

# # Input fields for email credentials
# from_email = st.text_input("Email Address")
# from_password = st.text_input("Password", type="password")
# if st.button("Fetch Emails"):
#     if not from_email or not from_password:
#         st.error("Please provide both email address and password.")
#     else:
#         # Fetch email data from the FastAPI API using provided credentials
#         response = requests.post(API_URL, json={"username": from_email, "password": from_password})
#         data = response.json()
#         emails = data.get("emails", [])

#         for email in emails:
#             st.write(f"From: {email['from']}")
#             st.write(f"Subject: {email['subject']}")
#             st.write(f"Content: {email['content']}")
#             st.write("-" * 50)

# ---------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests

# # Define the FastAPI API URLs
# SET_CREDENTIALS_URL = "http://localhost:8000/set-credentials"  # Endpoint to set credentials
# FETCH_EMAILS_URL = "http://localhost:8000/"  # Endpoint to fetch emails

# # Streamlit app
# st.title("Email Viewer")

# # Input fields for email credentials
# from_email = st.text_input("Email Address")
# from_password = st.text_input("Password", type="password")

# if st.button("Set Credentials"):
#     if not from_email or not from_password:
#         st.error("Please provide both email address and password.")
#     else:
#         # Set email credentials using the FastAPI endpoint
#         response = requests.post(SET_CREDENTIALS_URL, json={"username": from_email, "password": from_password})
#         if response.status_code == 200:
#             st.success("Credentials set successfully")
#         else:
#             st.error("Failed to set credentials")

# if st.button("Fetch Emails"):
#     # Fetch email data from the FastAPI API
#     response = requests.get(FETCH_EMAILS_URL)
#     data = response.json().get("emails", [])

#     for email in data:
#         st.write(f"From: {email['from']}")
#         st.write(f"Subject: {email['subject']}")
#         st.write(f"Content: {email['content']}")
#         st.write("-" * 50)

# ---------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests

# # Define the FastAPI API URLs
# SET_CREDENTIALS_URL = "http://localhost:8000/set-credentials"  # Endpoint to set credentials
# FETCH_EMAILS_URL = "http://localhost:8000/"  # Endpoint to fetch emails

# # Streamlit app
# st.title("Email Viewer")

# # Input fields for email credentials
# from_email = st.text_input("Email Address")
# from_password = st.text_input("Password", type="password")

# if st.button("Set Credentials"):
#     if not from_email or not from_password:
#         st.error("Please provide both email address and password.")
#     else:
#         # Set email credentials using the FastAPI endpoint
#         response = requests.post(SET_CREDENTIALS_URL, json={"username": from_email, "password": from_password})
#         if response.status_code == 200:
#             st.success("Credentials set successfully")
#         else:
#             st.error("Failed to set credentials")

# if st.button("Fetch Emails"):
#     # Fetch email data from the FastAPI API
#     response = requests.get(FETCH_EMAILS_URL)
#     data = response.json().get("emails", [])

#     for email in data:
#         # Create a collapsible section for each email
#         with st.beta_expander(f"From: {email['from']}, Subject: {email['subject']}"):
#             # Display the content of the email
#             st.write("Content:")
#             st.write(email['content'])

#             # Add a dropdown to view the summary
#             if st.checkbox("View Summary"):
#                 st.write("Summary:")
#                 st.write(email['summary'])

# ----------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests

# # Define the FastAPI API URLs
# SET_CREDENTIALS_URL = "http://localhost:8000/set-credentials"  # Endpoint to set credentials
# FETCH_EMAILS_URL = "http://localhost:8000/"  # Endpoint to fetch emails

# # Streamlit app
# st.title("Email Viewer")

# # Input fields for email credentials
# from_email = st.text_input("Email Address")
# from_password = st.text_input("Password", type="password")

# if st.button("Set Credentials"):
#     if not from_email or not from_password:
#         st.error("Please provide both email address and password.")
#     else:
#         # Set email credentials using the FastAPI endpoint
#         try:
#             response = requests.post(SET_CREDENTIALS_URL, json={"username": from_email, "password": from_password})
#             if response.status_code == 200:
#                 st.success("Credentials set successfully")
#             else:
#                 st.error("Failed to set credentials")
#         except Exception as e:
#             # Display error message and the humorous meme
#             st.error("Something went wrong. Please check your credentials.")
#             st.image("https://media.makeameme.org/created/something-went-wrong-45810703c6.jpg", use_column_width=True)

# if st.button("Fetch Emails"):
#     # Fetch email data from the FastAPI API
#     try:
#         response = requests.get(FETCH_EMAILS_URL)
#         data = response.json().get("emails", [])

#         for email in data:
#             # Create a collapsible section for each email
#             with st.beta_expander(f"From: {email['from']}, Subject: {email['subject']}"):
#                 # Display the content of the email
#                 st.write("Content:")
#                 st.write(email['content'])

#                 # Add a dropdown to view the summary
#                 if st.checkbox("View Summary"):
#                     st.write("Summary:")
#                     st.write(email['summary'])
#     except Exception as e:
#         # Display error message and the humorous meme
#         st.error("Something went wrong while fetching emails.")
#         st.image("https://media.makeameme.org/created/something-went-wrong-45810703c6.jpg", use_column_width=True)

# -------------------------------------------------------------------

# import streamlit as st
# import requests

# # Streamlit app
# st.title("Email Viewer")

# # Input fields for email credentials
# from_email = st.text_input("Email Address")
# from_password = st.text_input("Password", type="password")

# # Define the FastAPI API URLs
# SET_CREDENTIALS_URL = "http://localhost:8000/set-credentials"  # Endpoint to set credentials
# FETCH_EMAILS_URL = "http://localhost:8000/"  # Endpoint to fetch emails

# if st.button("Set Credentials"):
#     if not from_email or not from_password:
#         st.error("Please provide both email address and password.")
#     else:
#         # Set email credentials using the FastAPI endpoint
#         try:
#             response = requests.post(SET_CREDENTIALS_URL, json={"username": from_email, "password": from_password})

#             if response.status_code == 200:
#                 st.success(f"Credentials set successfully. Email: {from_email}, Password: {from_password}")
#             else:
#                 st.error("Failed to set credentials")
#         except Exception as e:
#             st.error("An error occurred while setting credentials.")

# if st.button("Fetch Emails"):
#     # Fetch email data from the FastAPI API
#     try:
#         response = requests.get(FETCH_EMAILS_URL)
#         if response.status_code == 200:
#             data = response.json().get("emails", [])

#             for email in data:
#                 # Create an expander section for each email
#                 with st.expander(f"**From**:\n{email['from']}\n\n**Subject**:\n{email['subject']}\n\n**Tags**:\n{email['tag']}"):

#                     # Display the summary of the email (not 'content')
#                     st.write("Summary:")
#                     st.write(email['summary'])
#         else:
#             st.error("Failed to fetch emails. Status code: " + str(response.status_code))
#     except Exception as e:
#         st.error("An error occurred while fetching emails: " + str(e))

# -------------------------------------------------------------------

# This code is upadted to fetch emails and render them correctky
# This is condeirng that emails returned are of follwoing structure
# emails:[{"subject":"abc","summary":"xyz","from":"abc@xyz","tag":"['tag1','tag2']"},{},{},....]

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
                    f"Credentials set successfully. Email: {from_email}, Password: {from_password}"
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

    print(
        f"{page_number = } \n {start_index = } \n {end_index = } \n {email_ids[0:20]} = "
    )

    email_messages = email_utils.decode_emails(email_ids, start_index, end_index,
                                               from_email, from_password)

    # Render the email messages for the current page.
    for email_message in email_messages:
        if "model" not in st.session_state.keys():
            st.session_state["model"] = LLM.init()
        model = st.session_state["model"]
        tags = LLM.get_tags(email_message["content"], model[1])
        spam = LLM.detect_spam(email_message["content"], model[0])
        with st.expander(f"**From**:\n{email_message['from']}\n\n**Subject**:\n{email_message['subject']}\n\n**Tags**:\n{tags[0]['generated_text']}\n\n{'***spam***' if spam == 'spam' else ''}"
                         ):

            st.markdown(f'**Body:** {email_message["content"]}')
            st.markdown(f"")

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
