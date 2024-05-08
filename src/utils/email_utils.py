import email
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

class GmailUtils:
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate with a Gmail account using IMAP.

        Args:
            username (str): The Gmail username.
            password (str): The Gmail password.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            logger.info("Successfully connected to Gmail IMAP server")
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to establish connection to Gmail IMAP server: {e}")
            return False

        try:
            imap_server.login(username, password)
            logger.info("Successfully logged in to Gmail IMAP server")
            imap_server.logout()
            return True
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to log in to Gmail IMAP server: {e}")
            return False

    @staticmethod
    def fetch_unread_emails(username, password):
        """
        Fetch unread emails from the primary category of the Gmail inbox.

        Args:
            username (str): The Gmail username.
            password (str): The Gmail password.

        Returns:
            list: A list of email IDs representing unread emails.
        """
        unread_emails = []
        try:
            imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            logger.info("Successfully connected to Gmail IMAP server")
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to establish connection to Gmail IMAP server: {e}")
            return unread_emails

        try:
            imap_server.login(username, password)
            logger.info("Successfully logged in to Gmail IMAP server")
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to log in to Gmail IMAP server: {e}")
            return unread_emails

        try:
            imap_server.select('INBOX')
            _, data = imap_server.search(None, 'X-GM-RAW', 'category:primary is:unread')
            if data:
                email_ids = data[0].split()
                unread_emails = [int(email_id) for email_id in email_ids]
                logger.info(f"Found {len(unread_emails)} unread emails in the Primary category")
            else:
                logger.info("No unread emails found in the Primary category")
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to search for unread emails: {e}")

        imap_server.logout()
        return unread_emails

    @staticmethod
    def fetch_emails(email_ids, start_idx, end_idx, username, password):
        """
        Fetch emails from the Gmail inbox based on the provided email IDs and range.

        Args:
            email_ids (list): List of email IDs to fetch.
            start_idx (int): Start index of the range to fetch.
            end_idx (int): End index of the range to fetch.
            username (str): The Gmail username.
            password (str): The Gmail password.

        Returns:
            list: A list of dictionaries representing the fetched emails.
        """
        fetched_emails = []
        try:
            imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to establish connection to Gmail IMAP server: {e}")
            return fetched_emails

        try:
            imap_server.login(username, password)
            logger.info("Successfully logged in to Gmail IMAP server")
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to log in to Gmail IMAP server: {e}")
            return fetched_emails

        try:
            imap_server.select('INBOX')
            for idx in range(start_idx, min(end_idx, len(email_ids))):
                email_id = email_ids[idx]
                _, data = imap_server.fetch(str(email_id), '(RFC822)')
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
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            email_info['Content'] = part.get_payload(decode=True).decode(part.get_content_charset())
                        elif part.get_content_maintype() == 'multipart':
                            continue
                        elif part.get('Content-Disposition') is not None:
                            attachment = {
                                'Filename': part.get_filename(),
                                'Content-Type': part.get_content_type(),
                                'Content': part.get_payload(decode=True)
                            }
                            email_info['Attachments'].append(attachment)
                    fetched_emails.append(email_info)
        except imaplib.IMAP4.error as e:
            logger.error(f"Failed to fetch emails: {e}")

        imap_server.logout()
        return fetched_emails

class MLStripper(HTMLParser):
    """
    A subclass of HTMLParser used to strip HTML tags from HTML content.
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        """
        Override handle_data method to extract text data from HTML content.
        """
        self.fed.append(d)

    def get_data(self):
        """
        Get the stripped text data.
        """
        return ''.join(self.fed)

def strip_tags(html):
    """
    Strip HTML tags from HTML strings.

    Args:
        html (str): The HTML string to strip tags from.

    Returns:
        str: The text content without HTML tags.
    """
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()

# Example usage
if __name__ == "__main__":
    username = input("Enter your Gmail username: ")
    password = input("Enter your Gmail password: ")

    if GmailUtils.authenticate(username, password):
        print("Authentication successful")
        unread_email_ids = GmailUtils.fetch_unread_emails(username, password)
        print("Unread email IDs:", unread_email_ids)

        start_idx = int(input("Enter the start index: "))
        end_idx = int(input("Enter the end index: "))
        fetched_emails = GmailUtils.fetch_emails(unread_email_ids, start_idx, end_idx, username, password)
        print("Fetched emails:", fetched_emails)

        html_content = "<p>Hello <strong>world</strong>!</p>"
        text_content = strip_tags(html_content)
        print("Stripped text:", text_content)
    else:
        print("Authentication failed")
