import email
import asyncio
import logging
import imaplib
from html.parser import HTMLParser
from email.header import decode_header
from email.utils import parsedate_to_datetime

# IMAP server details
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("./logs/email_utils.log"),
        logging.StreamHandler()
    ],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GmailClient:
    """
    Class to interact with Gmail IMAP server for fetching emails.
    """

    def __init__(self, username, password):
        """
        Initialize GmailClient with username and password.
        """
        self.username = username
        self.password = password
        self.imap_server = None

    async def connect(self):
        """
        Connect to the Gmail IMAP server.
        """
        try:
            self.imap_server = await asyncio.wait_for(
                asyncio.to_thread(imaplib.IMAP4_SSL, IMAP_SERVER, IMAP_PORT), timeout=10
            )
            self.imap_server.login(self.username, self.password)
            logger.info("Successfully connected to and logged in to Gmail IMAP server")
            return True
        except (imaplib.IMAP4.error, asyncio.TimeoutError) as e:
            logger.error(f"Failed to connect to Gmail IMAP server: {e}")
            return False

    def disconnect(self):
        """
        Disconnect from the Gmail IMAP server.
        """
        if self.imap_server:
            self.imap_server.logout()
            logger.info("Disconnected from Gmail IMAP server")

    async def fetch_unread_email_ids(self):
        """
        Fetch IDs of unread emails from the Gmail inbox.
        """
        if not self.imap_server:
            logger.error("IMAP server not connected")
            return []

        try:
            self.imap_server.select('INBOX')
            _, data =self.imap_server.search(None, 'X-GM-RAW', 'Category:Primary', 'UNSEEN')
            if data:
                return [int(email_id) for email_id in data[0].split()]
            else:
                logger.info("No unread emails found in the Primary category")
                return []
        except (imaplib.IMAP4.error, asyncio.TimeoutError) as e:
            logger.error(f"Failed to search for unread emails: {e}")
            return []

    async def fetch_email(self, email_id):
        """
        Fetch details of a specific email.
        """
        if not self.imap_server:
            logger.error("IMAP server not connected")
            return None

        try:
            self.imap_server.select('INBOX', readonly=True)
            _, data = self.imap_server.fetch(str(email_id), '(RFC822)')
            if data:
                raw_email = data[0][1]
                message = email.message_from_bytes(raw_email)
                email_info = {
                    'Message-ID': message.get('Message-ID'),
                    'In-Reply-To': message.get('In-Reply-To'),
                    'Subject': decode_header(message['Subject'])[0][0],
                    'Sender': message['From'],
                    'Date': parsedate_to_datetime(message['Date']),
                    'Content': '',
                    'Attachments': []
                }
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            email_info['Content'] = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        elif part.get_content_maintype() == 'multipart':
                            continue
                        elif part.get('Content-Disposition') is not None:
                            attachment = {
                                'Filename': part.get_filename(),
                                'Content-Type': part.get_content_type(),
                                'Content': part.get_payload(decode=True)
                            }
                            email_info['Attachments'].append(attachment)
                else:
                    email_info['Content'] = message.get_payload(decode=True).decode('utf-8', errors='ignore')
                return email_info
        except (imaplib.IMAP4.error, asyncio.TimeoutError) as e:
            logger.error(f"Failed to fetch email {email_id}: {e}")
            return None


class MLStripper(HTMLParser):
    """
    HTML tag stripper.
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        """
        Handle HTML data.
        """
        self.fed.append(d)

    def get_data(self):
        """
        Get stripped HTML data.
        """
        return ''.join(self.fed)

def strip_tags(html):
    """
    Strip HTML tags from HTML strings.
    """
    if html.startswith("<html>"):
        stripper = MLStripper()
        stripper.feed(html)
        return stripper.get_data()
    else:
        return html

if __name__ == "__main__":
    
    # Test the GmailClient class
    async def main():
        username = input("Enter your Gmail username: ")
        password = input("Enter your Gmail password: ")

        # Test the GmailClient class
        gmail_client = GmailClient(username, password)
        if await gmail_client.connect():
            unread_email_ids = await gmail_client.fetch_unread_email_ids()
            if unread_email_ids:
                print("Unread email IDs:", unread_email_ids)
                start_idx = int(input("Enter the start index: "))
                end_idx = int(input("Enter the end index: "))
                tasks = [gmail_client.fetch_email(email_id) for email_id in unread_email_ids[start_idx:end_idx]]
                fetched_emails = await asyncio.gather(*tasks)
                print("Fetched emails:", fetched_emails)
            else:
                print("No unread emails found")
            gmail_client.disconnect()
        else:
            print("Authentication failed")

    asyncio.run(main())
    
    # Test the strip_tags function
    html = "<p>This is a <strong>test</strong> HTML string</p>"
    print(strip_tags(html))
    