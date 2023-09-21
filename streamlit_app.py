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

# Streamlit app
st.title("Email Viewer")

# Input fields for email credentials
from_email = st.text_input("Email Address")
from_password = st.text_input("Password", type="password")

# Define the FastAPI API URLs
SET_CREDENTIALS_URL = "http://localhost:8000/set-credentials"  # Endpoint to set credentials
FETCH_EMAILS_URL = "http://localhost:8000/"  # Endpoint to fetch emails

if st.button("Set Credentials"):
    if not from_email or not from_password:
        st.error("Please provide both email address and password.")
    else:
        # Set email credentials using the FastAPI endpoint
        try:
            response = requests.post(SET_CREDENTIALS_URL, json={"username": from_email, "password": from_password})
            
            if response.status_code == 200:
                st.success(f"Credentials set successfully. Email: {from_email}, Password: {from_password}")
            else:
                st.error("Failed to set credentials")
        except Exception as e:
            st.error("An error occurred while setting credentials.")

if st.button("Fetch Emails"):
    # Fetch email data from the FastAPI API
    try:
        response = requests.get(FETCH_EMAILS_URL)
        if response.status_code == 200:
            data = response.json().get("emails", [])
    
            for email in data:
                # Create an expander section for each email
                tag_list = email['tag'].strip("[]").replace("'", "").split(',')

# Strip leading and trailing spaces from each tag and join them with a comma and a space
                tag_string = ", ".join(tag.strip() for tag in tag_list)
               
                with st.expander(f"**From**:\n{email['from']}\n\n**Subject**:\n{email['subject']}\n\n**Tags**:\n{tag_string}"):
                    
                    st.write("Summary:")
                    st.write(email['summary'])
        else:
            st.error("Failed to fetch emails. Status code: " + str(response.status_code))
    except Exception as e:
        st.error("An error occurred while fetching emails: " + str(e))
