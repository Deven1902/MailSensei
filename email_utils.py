import email
import imaplib
from LLM import Summarizer

# llm = Summarizer()


def set_credentials(username, password):
  """Sets the IMAP credentials. and check if the credentials are valid.

    Args:
      username: The Gmail username.
      password: The Gmail password.
    """
  try:
    imap_server = 'imap.gmail.com'
    imap_port = 993

    # Create an IMAP connection.
    imap_connection = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Login to the IMAP server.
    imap_connection.login(username, password)
    return True
  except:
    return False


def fetch_emails_from_imap(username, password, page_number=1, page_size=10):
  """Fetches emails from IMAP with pagination.

    Args:
      username: The Gmail username.
      password: The Gmail password.
      page_number: The current page number.
      page_size: The number of emails to display per page.

    Returns:
      A list of email messages.
    """

  imap_server = 'imap.gmail.com'
  imap_port = 993

  # Create an IMAP connection.
  imap_connection = imaplib.IMAP4_SSL(imap_server, imap_port)

  # Login to the IMAP server.
  imap_connection.login(username, password)
  # print(f"{imap_connection.list()[1][0] = }")
  # Select the INBOX mailbox.
  imap_connection.select('INBOX')
  
  # Search for all unread emails.
  emails = imap_connection.search(None, 'X-GM-RAW "Category:Primary"')
  # Get the email IDs.

  email_ids = emails[1][0].decode().split(' ')
  # Get the email messages for the current page.
  imap_connection.close()

  return email_ids


def decode_emails(email_ids, start_index, end_index, username,password):
  imap_server = 'imap.gmail.com'
  imap_port = 993

  # Create an IMAP connection.
  imap_connection = imaplib.IMAP4_SSL(imap_server, imap_port)
  imap_connection.login(username, password)
  imap_connection.select('INBOX')
  email_messages = []
  for email_id in email_ids[start_index:end_index]:
    email_message = imap_connection.fetch(email_id, '(RFC822)')[1][0][1]
    msg = email.message_from_string(
        email_message.decode('utf-8', errors='ignore'))
    email_subject = msg['subject']
    email_from = msg['from']
    email_content = ""

    if msg.is_multipart():
      for part in msg.walk():
        if part.get_content_type() == "text/plain":
          email_content = part.get_payload(decode=True).decode('utf-8',
                                                               errors='ignore')
          break
    else:
      email_content = msg.get_payload(decode=True).decode('utf-8',
                                                          errors='ignore')

    # Extract Message-ID, In-Reply-To, and References headers
    message_id = msg.get("Message-ID", "")
    in_reply_to = msg.get("In-Reply-To", "")

    # Identify the thread or create a new one
    SingleEmail = {
        'Message ID': message_id,
        'from': email_from,
        'subject': email_subject,
        'content': email_content,
        'IsReply': bool(in_reply_to),  # Check if it's a reply
        'InReplyTo': in_reply_to,  # Add the ID of the parent message
        'StoreReplyThread': [],
        # 'summary': llm.summarize(email_content)
    }

    email_messages.append(SingleEmail)

  # Close the IMAP connection.
  imap_connection.close()
  
  return email_messages
