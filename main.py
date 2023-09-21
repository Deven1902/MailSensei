# from fastapi import FastAPI
# from fastapi import Depends
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# app = FastAPI()

# # # Python 3.8.0
# import smtplib
# import time
# import imaplib
# import email
# import traceback 
# # -------------------------------------------------
# #
# # Utility to read email from Gmail Using Python
# #
# # ------------------------------------------------
# ORG_EMAIL = "@gmail.com" 
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL 
# FROM_PWD = "Atharv@15" 
# SMTP_SERVER = "imap.gmail.com" 
# SMTP_PORT = 993

# # def read_email_from_gmail():
# #     try:
# #         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
# #         mail.login(FROM_EMAIL,FROM_PWD)
# #         mail.select('inbox')

# #         data = mail.search(None, 'ALL')
# #         mail_ids = data[1]
# #         id_list = mail_ids[0].split()   
# #         first_email_id = int(id_list[0])
# #         latest_email_id = int(id_list[-1])

# #         for i in range(latest_email_id,first_email_id, -1):
# #             data = mail.fetch(str(i), '(RFC822)' )
# #             for response_part in data:
# #                 arr = response_part[0]
# #                 if isinstance(arr, tuple):
# #                     msg = email.message_from_string(str(arr[1],'utf-8'))
# #                     email_subject = msg['subject']
# #                     email_from = msg['from']
# #                     print('From : ' + email_from + '\n')
# #                     print('Subject : ' + email_subject + '\n')

# #     except Exception as e:
# #         traceback.print_exc() 
# #         print(str(e))

# # read_email_from_gmail()

# # Importing libraries
# import imaplib, email

# user = 'USER_EMAIL_ADDRESS'
# password = 'USER_PASSWORD'
# imap_url = 'imap.gmail.com'

# # Function to get email content part i.e its body part
# def get_body(msg):
# 	if msg.is_multipart():
# 		return get_body(msg.get_payload(0))
# 	else:
# 		return msg.get_payload(None, True)

# # Function to search for a key value pair
# def search(key, value, con):
# 	result, data = con.search(None, key, '"{}"'.format(value))
# 	return data

# # Function to get the list of emails under this label
# def get_emails(result_bytes):
# 	msgs = [] # all the email data are pushed inside an array
# 	for num in result_bytes[0].split():
# 		typ, data = con.fetch(num, '(RFC822)')
# 		msgs.append(data)

# 	return msgs

# # this is done to make SSL connection with GMAIL
# con = imaplib.IMAP4_SSL(imap_url)

# # logging the user in
# con.login(user, password)

# # calling function to check for email under this label
# con.select('Inbox')

# # fetching emails from this user "tu**h*****1@gmail.com"
# msgs = get_emails(search('FROM', 'MY_ANOTHER_GMAIL_ADDRESS', con))

# # Uncomment this to see what actually comes as data
# # print(msgs)


# # Finding the required content from our msgs
# # User can make custom changes in this part to
# # fetch the required content he / she needs

# # printing them by the order they are displayed in your gmail
# for msg in msgs[::-1]:
# 	for sent in msg:
# 		if type(sent) is tuple:

# 			# encoding set as utf-8
# 			content = str(sent[1], 'utf-8')
# 			data = str(content)

# 			# Handling errors related to unicodenecode
# 			try:
# 				indexstart = data.find("ltr")
# 				data2 = data[indexstart + 5: len(data)]
# 				indexend = data2.find("</div>")

# 				# printing the required content which we need
# 				# to extract from our email i.e our body
# 				print(data2[0: indexend])

# 			except UnicodeEncodeError as e:
# 				pass


# @app.get("/")
# def read():
#     return read_email_from_gmail()


# from fastapi import FastAPI

# import imaplib
# import email
# import traceback

# app = FastAPI()


# # hcchlheuhygtengq
# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL  # Replace with your Gmail email address
# FROM_PWD = "hcchlheuhygtengq"  # Replace with your Gmail password
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# # Function to read emails from Gmail
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         data = mail.search(None, 'ALL')
#         mail_ids = data[1]
#         id_list = mail_ids[0].split()
#         first_email_id = int(id_list[0])
#         latest_email_id = int(id_list[-1])

#         emails = []

#         for i in range(latest_email_id, first_email_id - 1, -1):
#             data = mail.fetch(str(i), '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = msg.get_payload(decode=True).decode('utf-8')
#                     emails.append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content
#                     })

#         return emails

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     emails = read_email_from_gmail()
#     return {"emails": emails}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





# IMP
# from fastapi import FastAPI
# import imaplib
# import email
# import traceback
# from datetime import datetime

# app = FastAPI()

# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL
# FROM_PWD = "hcchlheuhygtengq"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# # Function to read emails from Gmail for today's date
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         today = datetime.now().strftime("%d-%b-%Y")

#         # Search for emails sent on today's date
#         result, data = mail.search(None, 'ON', today)
#         email_ids = data[0].split()

#         emails = []

#         for email_id in email_ids:
#             data = mail.fetch(email_id, '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = ""

#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
#                                 break
#                     else:
#                         email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

#                     emails.append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content
#                     })

#         return emails

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     emails = read_email_from_gmail()
#     return {"emails": emails}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# from fastapi import FastAPI
# import imaplib
# import email
# import traceback
# from datetime import datetime

# app = FastAPI()

# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL
# FROM_PWD = "hcchlheuhygtengq"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# # Function to read emails from Gmail for today's date and group them by threads
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         today = datetime.now().strftime("%d-%b-%Y")

#         # Search for emails sent on today's date
#         result, data = mail.search(None, 'ON', today)
#         email_ids = data[0].split()

#         threads = {}

#         for email_id in email_ids:
#             data = mail.fetch(email_id, '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = ""

#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
#                                 break
#                     else:
#                         email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

#                     # Extract Message-ID and References headers
#                     message_id = msg.get("Message-ID", "")
#                     references = msg.get("References", "").split()

#                     # Identify the thread or create a new one
#                     thread = threads.get(message_id, {"message_id": message_id, "emails": []})
#                     thread["emails"].append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content
#                     })

#                     # Update the thread's dictionary
#                     threads[message_id] = thread

#                     # Link references to the same thread
#                     for ref in references:
#                         if ref:
#                             threads[ref] = thread

#         return list(threads.values())

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     threads = read_email_from_gmail()
#     return {"threads": threads}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# from fastapi import FastAPI
# import imaplib
# import email
# import traceback
# from datetime import datetime

# app = FastAPI()

# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL
# FROM_PWD = "hcchlheuhygtengq"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# # Function to read the latest 5 emails from Gmail for today's date
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         today = datetime.now().strftime("%d-%b-%Y")

#         # Search for emails sent on today's date
#         result, data = mail.search(None, 'ON', today)
#         email_ids = data[0].split()
        
#         # Reverse the list to get the latest emails first
#         email_ids.reverse()

#         # Limit the loop to the first 5 email IDs
#         email_ids = email_ids[:5]

#         threads = {}

#         for email_id in email_ids:
#             data = mail.fetch(email_id, '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = ""

#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
#                                 break
#                     else:
#                         email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

#                     # Extract Message-ID and References headers
#                     message_id = msg.get("Message-ID", "")
#                     references = msg.get("References", "").split()

#                     # Identify the thread or create a new one
#                     thread = threads.get(message_id, {"message_id": message_id, "emails": []})
#                     thread["emails"].append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content
#                     })

#                     # Update the thread's dictionary
#                     threads[message_id] = thread

#                     # Link references to the same thread
#                     for ref in references:
#                         if ref:
#                             threads[ref] = thread

#         return list(threads.values())

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     threads = read_email_from_gmail()
#     return {"threads": threads}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# from fastapi import FastAPI
# import imaplib
# import email
# import traceback
# from datetime import datetime

# app = FastAPI()

# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL
# FROM_PWD = "hcchlheuhygtengq"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# # Function to read the latest 5 emails from Gmail for today's date
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         today = datetime.now().strftime("%d-%b-%Y")

#         # Search for emails sent on today's date
#         result, data = mail.search(None, 'ON', today)
#         email_ids = data[0].split()
        
#         # Reverse the list to get the latest emails first
#         email_ids.reverse()

#         # Limit the loop to the first 5 email IDs
#         email_ids = email_ids[:5]

#         threads = {}

#         for email_id in email_ids:
#             data = mail.fetch(email_id, '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = ""

#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
#                                 break
#                     else:
#                         email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

#                     # Extract Message-ID and In-Reply-To headers
#                     message_id = msg.get("Message-ID", "")
#                     in_reply_to = msg.get("In-Reply-To", "")
                    
#                     # Identify the thread or create a new one
#                     thread = threads.get(message_id, {"message_id": message_id, "emails": []})
#                     thread["emails"].append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content
#                     })

#                     # Update the thread's dictionary
#                     threads[message_id] = thread

#                     # Link replies to the parent email thread
#                     if in_reply_to:
#                         parent_thread = threads.get(in_reply_to)
#                         if parent_thread:
#                             parent_thread["emails"].extend(thread["emails"])
#                             threads[in_reply_to] = parent_thread

#         return list(threads.values())

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     threads = read_email_from_gmail()
#     return {"threads": threads}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# -----------------------------------------


# from fastapi import FastAPI
# import imaplib
# import email
# import traceback
# from datetime import datetime

# app = FastAPI()

# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL
# FROM_PWD = "hcchlheuhygtengq"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# # Function to read the latest 5 emails from Gmail for today's date
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         today = datetime.now().strftime("%d-%b-%Y")

#         # Search for emails sent on today's date
#         result, data = mail.search(None, 'ON', today)
#         email_ids = data[0].split()
        
#         # Reverse the list to get the latest emails first
#         email_ids.reverse()

#         # Limit the loop to the first 5 email IDs
#         email_ids = email_ids[:5]

#         threads = {}

#         for email_id in email_ids:
#             data = mail.fetch(email_id, '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = ""

#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
#                                 break
#                     else:
#                         email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

#                     # Extract Message-ID, In-Reply-To, and References headers
#                     message_id = msg.get("Message-ID", "")
#                     in_reply_to = msg.get("In-Reply-To", "")
                    
#                     # Identify the thread or create a new one
#                     thread = threads.get(message_id, {"message_id": message_id, "emails": []})
#                     thread["emails"].append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content,
#                         'IsReply': bool(in_reply_to)  # Check if it's a reply
#                     })

#                     # Update the thread's dictionary
#                     threads[message_id] = thread

#                     # Link replies to the parent email thread
#                     if in_reply_to:
#                         parent_thread = threads.get(in_reply_to)
#                         if parent_thread:
#                             parent_thread["emails"].extend(thread["emails"])
#                             threads[in_reply_to] = parent_thread

#         return list(threads.values())

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     threads = read_email_from_gmail()
#     return {"threads": threads}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# --------------------------------------------------------------

































# from fastapi import FastAPI
# import imaplib
# import email
# import traceback
# from datetime import datetime
# import json

# app = FastAPI()

# # Gmail configuration
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "atharvnodejsassignment" + ORG_EMAIL
# FROM_PWD = "hcchlheuhygtengq"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

# StoreMsgIds=[]

# StoreReplyThread=[]

# def organize_reply_threads(threads):
#     try:
#         for eachEmailInfo in threads:
#             StoreMsgIds.append(eachEmailInfo['message_id'])



#     except Exception as e:
#         traceback.print_exc()
#         return str(e)




# # Function to read the latest 5 emails from Gmail for today's date
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')

#         today = datetime.now().strftime("%d-%b-%Y")

#         # Search for emails sent on today's date
#         result, data = mail.search(None, 'ON', today)
#         email_ids = data[0].split()
        
#         # Reverse the list to get the latest emails first
#         email_ids.reverse()

#         # Limit the loop to the first 5 email IDs
#         email_ids = email_ids[:5]

#         threads = {}

#         for email_id in email_ids:
#             data = mail.fetch(email_id, '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_content = ""

#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
#                                 break
#                     else:
#                         email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

#                     # Extract Message-ID, In-Reply-To, and References headers
#                     message_id = msg.get("Message-ID", "")
#                     in_reply_to = msg.get("In-Reply-To", "")
                    
#                     # Identify the thread or create a new one
#                     thread = threads.get(message_id, {"message_id": message_id, "emails": []})
#                     thread["emails"].append({
#                         'from': email_from,
#                         'subject': email_subject,
#                         'content': email_content,
#                         'IsReply': bool(in_reply_to),  # Check if it's a reply
#                         'InReplyTo': in_reply_to,  # Add the ID of the parent message
#                         'StoreReplyThread':StoreReplyThread
#                     })

#                     # Update the thread's dictionary
#                     threads[message_id] = thread

#                     # Link replies to the parent email thread
#                     if in_reply_to:
#                         parent_thread = threads.get(in_reply_to)
#                         if parent_thread:
#                             parent_thread["emails"].extend(thread["emails"])
#                             threads[in_reply_to] = parent_thread

#         return list(threads.values())

#     except Exception as e:
#         traceback.print_exc()
#         return str(e)

# @app.get("/")
# def read():
#     threads = read_email_from_gmail()
#     # organize_reply_threads(threads)
#     return {"threads": threads}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI
import imaplib
import email
import traceback
from datetime import datetime
import json
from typing import List


app = FastAPI()

def tag_generator(email):
    llm=OpenAI(model_name='gpt-3.5-turbo',temperature=1,max_tokens=256)
    templates={
        'tag':"Please select the most appropriate tag from the following list to describe the email:\n\n" \
           "Funding\n" \
           "Product Development\n" \
           "Client Communication\n" \
           "Sales and Revenue\n" \
           "Tech Support\n" \
           "Marketing\n" \
           "Hiring\n" \
           "Legal and Compliance\n" \
           "Strategic Planning\n" \
           "Spam\n" \
           "\nAdditionally, the email body is as follows: {email}"
    }
    outputs = {}

    for key, template in templates.items():
        prompt = PromptTemplate(input_variables=["email"], template=template)
        chain = LLMChain(llm=llm, prompt=prompt)
        output = chain.run(email=email)
        outputs[key] = output

    tag_output = outputs.get('tag', 'Misceallaneous')

    return tag_output



def email_summarizer(subject,email):
    llm = OpenAI(model_name='gpt-3.5-turbo', temperature=1, max_tokens=256)

    templates = {
    #     'summary': "Write a brief summary from the following subject in 3 lines only focus on the important part don't include things like the name of receiver and other stuff not related to the main idea of the email: {subject}\n\n and email:\n\n{email}\n\nSummary:",
    #    'tag':"Please select the most appropriate tag from the following list to describe the email:\n\n" \
    #        "Funding\n" \
    #        "Product Development\n" \
    #        "Client Communication\n" \
    #        "Sales and Revenue\n" \
    #        "Tech Support\n" \
    #        "Marketing\n" \
    #        "Hiring\n" \
    #        "Legal and Compliance\n" \
    #        "Strategic Planning\n" \
    #        "Spam\n" \
    #        "\nAdditionally, the email body is as follows: {email}"
    'summary': "Write a brief summary from the following subject in 3 lines only focus on the important part don't include things like the name of the receiver and other stuff not related to the main idea of the email: {subject}\n\n and email:\n\n{email}\n\nSummary:",
    # 'tag': "Please select the most appropriate tag from the following list to describe the email:\n\n"
    #        "Funding\n"
    #        "Product Development\n"
    #        "Client Communication\n"
    #        "Sales and Revenue\n"
    #        "Tech Support\n"
    #        "Marketing\n"
    #        "Hiring\n"
    #        "Legal and Compliance\n"
    #        "Strategic Planning\n"
    #        "Spam\n"
    #        "\nAdditionally, the email body is as follows: {email}"
    }

    outputs = {}

    for key, template in templates.items():
        prompt = PromptTemplate(input_variables=["email","subject"], template=template)
        chain = LLMChain(llm=llm, prompt=prompt)
        output = chain.run(email=email, subject=subject)
        outputs[key] = output

    summary_output = outputs.get('summary', 'Summary not available')
    tag_output=outputs.get('tag','Misceallaneous')

    generated_tag=tag_generator(email)

    result = {
        'subject': subject,
        'summary': summary_output,
        'tag': generated_tag
    }

    return result

   
    # llm = OpenAI(model_name='gpt-3.5-turbo', temperature=1, max_tokens=256)

    # templates = {
    #     'summary': "Write a brief summary from the following subject in 3 lines only, focus on the important part, and don't include things like the name of the receiver and other stuff not related to the main idea of the email: {subject}\n\n and email:\n\n{email}\n\nSummary:",
    #     'tag_query': "Generate a tag for this email based on its content: {email}\n\nTag:"
    # }

    # outputs = {}

    # for key, template in templates.items():
    #     prompt = PromptTemplate(input_variables=["email", "subject"], template=template)
    #     chain = LLMChain(llm=llm, prompt=prompt)
    #     output = chain.run(email=email, subject=subject)
    #     outputs[key] = output

    # summary_output = outputs.get('summary', 'Summary not available')
    # tag_query_output = outputs.get('tag_query', 'Tag query not available')

    # # Extract the generated tag from the tag_query_output
    # generated_tag = tag_query_output.strip()

    # result = {
    #     'subject': subject,
    #     'summary': summary_output,
    #     'tag': generated_tag
    # }

    # return result


# def helper(emails,ReplyEmail,ReplyId):
#     try:
#       for email in emails:
#           if email['Message-ID']==ReplyId & email['IsReply']==false:
#               email.StoreReplyThread.append(ReplyEmail)
       
#       return emails


#     except Exception as e:
#         traceback.print_exc()
#         return str(e)


# def organize_reply_threads(emails):
#     try:
#         for email in emails:
#             if email['IsReply'] == True:
#                 EmailObj={
#                     'from': email['from'],
#                     'subject': email['subject'],
#                         'content': email['content']
#                 }
#                 FinalEmails=helper(emails,EmailObj,email['InReplyTo'])

#         return FinalEmails
                
            
#     except Exception as e:
#         traceback.print_exc()
#         return str(e)


def helper(emails, ReplyEmail, ReplyId):
    try:
        for email in emails:
            if email['Message ID'] == ReplyId and not email['IsReply']:
                email['StoreReplyThread'].append(ReplyEmail)

        return emails

    except Exception as e:
        traceback.print_exc()
        return str(e)

def organize_reply_threads(emails):
    try:
        for email in emails:
            if email['IsReply']==True:
                EmailObj = {
                    'from': email['from'],
                    'subject': email['subject'],
                    'content': email['content']
                }
                emails = helper(emails, EmailObj, email['InReplyTo'])
                emails.remove(email)

        return emails

    except Exception as e:
        traceback.print_exc()
        return str(e)
        
    
# Function to read the latest 5 emails from Gmail for today's date
def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        today = datetime.now().strftime("%d-%b-%Y")

        # Search for emails sent on today's date
        result, data = mail.search(None,'ALL', 'ON', today)
        email_ids = data[0].split()

        # print(email_ids)

        # Reverse the list to get the latest emails first
        email_ids.reverse()

        # Limit the loop to the first 5 email IDs
        # email_ids = email_ids[:5]

        emails = []

        for email_id in email_ids:
            data = mail.fetch(email_id, '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(arr[1].decode('utf-8', errors='ignore'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_content = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                email_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                    else:
                        email_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

                    # Extract Message-ID, In-Reply-To, and References headers
                    message_id = msg.get("Message-ID", "")
                    in_reply_to = msg.get("In-Reply-To", "")

                    # Identify the thread or create a new one
                    SingleEmail = {
                        'Message ID':msg.get("Message-ID", ""),
                        'from': email_from,
                        'subject': email_subject,
                        'content': email_content,
                        'IsReply': bool(in_reply_to),  # Check if it's a reply
                        'InReplyTo': in_reply_to,  # Add the ID of the parent message
                        'StoreReplyThread': []
                    }

                    emails.append(SingleEmail)

        return emails

    except Exception as e:
        traceback.print_exc()
        return str(e)

superFinalEmails=[]
@app.get("/")
def read():
    emails = read_email_from_gmail()
    finalEmails=organize_reply_threads(emails)
    return {{
  "emails": [
    {
      "subject": "Assistance Needed for Technical Issue",
      "summary": "The sender is requesting assistance for a technical issue they are experiencing with a product or service. They are asking for guidance and support, including the possibility of a support call or remote session. They express their appreciation for the recipient's prompt attention to the matter.",
      "tag": "Tech Support",
      "from": "Deven Nandapurkar <devenamazingnandapurkar@gmail.com>"
    },
    {
      "subject": "Business Development Intern Hiring",
      "summary": "The email expresses interest in a Business Development Intern position at Microsoft. The sender has a strong academic background in business development and has gained practical experience through extracurricular activities. They have experience in marketing, sales, and negotiation, as well as developing and executing marketing campaigns and creating a winning business plan.",
      "tag": "Hiring",
      "from": "Deven Nandapurkar <devenamazingnandapurkar@gmail.com>"
    },
    {
      "subject": "hi",
      "summary": "The email discusses Harvey Specter, a fictional lawyer known for his sharp suits, wit, and ability to close any deal. He is a partner at a prestigious law firm, known for his negotiating skills and ability to see through lies. Harvey also mentors a young man without a law degree, teaching him about the law. Harvey is a complex character, brilliant but arrogant and ruthless, yet loyal to his friends and always fighting for what he believes in. Some of his famous quotes are mentioned.",
      "tag": "Spam",
      "from": "Deven Nandapurkar <devennandapurkar2020.comp@mmcoe.edu.in>"
    }
  ]
}}
    for email in finalEmails:
        receivedEmail=email_summarizer(email['subject'],email['content'])
        emailobj={**receivedEmail,
                  'from':email['from']
                  }
        superFinalEmails.append(emailobj)
    return {'emails':superFinalEmails}

@app.post("/set-credentials")
async def set_credentials(credentials: dict):
    global FROM_EMAIL, FROM_PWD
    FROM_EMAIL = credentials.get("username")
    FROM_PWD = credentials.get("password")
    return {"message": "Credentials set successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
