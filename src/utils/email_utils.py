import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

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
            imap_server = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
            imap_server.login(username, password)
            imap_server.logout()
            print("Successfully authenticated with Gmail IMAP server")
            return True
        except imaplib.IMAP4.error as e:
            print(f"Failed to authenticate with Gmail IMAP server: {e}")
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
            imap_server = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
            imap_server.login(username, password)
            _, data = imap_server.search(None, 'X-GM-RAW', 'category:primary is:unread')
            imap_server.logout()
            if data:
                unread_emails = [int(email_id) for email_id in data[0].split()]
                print(f"Found {len(unread_emails)} unread emails in the Primary category")
            else:
                print("No unread emails found in the Primary category")
        except imaplib.IMAP4.error as e:
            print(f"Failed to fetch unread emails: {e}")
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
            imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
            imap_server.login(username, password)
            for idx in range(start_idx, min(end_idx, len(email_ids))):
                email_id = email_ids[idx]
                _, data = imap_server.fetch(str(email_id), '(RFC822)')
                if data:
                    raw_email = data[0][1]
                    message = email.message_from_bytes(raw_email)
                    email_info = GmailUtils.extract_email_info(message)
                    fetched_emails.append(email_info)
            imap_server.logout()
        except imaplib.IMAP4.error as e:
            print(f"Failed to fetch emails: {e}")
        return fetched_emails

    @staticmethod
    def extract_email_info(message):
        """
        Extract relevant information from an email message.

        Args:
            message (email.message.Message): Email message object.

        Returns:
            dict: Dictionary representing the extracted email information.
        """
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
        return email_info

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
        unread_email_ids = GmailUtils.fetch_unread_emails(username, password)
        print("Unread email IDs:", unread_email_ids)
        
        start_idx = int(input("Enter the start index: "))
        end_idx = int(input("Enter the end index: "))
        fetched_emails = GmailUtils.fetch_emails(unread_email_ids,
                                                 start_idx,
                                                 end_idx,
                                                 username,
                                                 password)
        print("Fetched emails:", fetched_emails)
        
        html_content = "<p>Hello <strong>world</strong>!</p>"
        text_content = strip_tags(html_content)
        print("Stripped text:", text_content)
