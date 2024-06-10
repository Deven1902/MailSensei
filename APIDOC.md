## Endpoints

### Setup Gmail Credentials
- **Method:** POST
- **Description:** Setup Gmail Credentials for accessing the Gmail IMAP server securely.
- **Request Body:**
    ```json
    {
        "gmail_address": "<gmail_address>",
        "app_password": "<app_password>"
    }
    ```
- **Response:**
    ```json
    {
        "success": true/false,
        "message": "<success/error_message>"
    }
    ```

### Connect to Gmail IMAP Server
- **Method:** POST
- **Description:** Establish a connection to the Gmail IMAP server.
- **Request Body:**
    ```json
    {
        "username": "<username>",
        "password": "<password>"
    }
    ```
- **Response:**
    ```json
    {
        "success": true/false,
        "message": "<success/error_message>"
    }
    ```

### Fetch IDs of Unread Emails
- **Method:** GET
- **Description:** Fetch IDs of unread emails from the Gmail inbox.
- **Response:**
    ```json
    [email_id1, email_id2, ...]
    ```

### Fetch Details of a Specific Email
- **Method:** GET
- **Description:** Fetch details of a specific email by its ID.
- **Path Parameter:**
    - `email_id`: ID of the email to fetch details for.
- **Response:**
    ```json
    {
        "Message-ID": "<message_id>",
        "Subject": "<subject>",
        "Sender": "<sender_email>",
        "Date": "<date>",
        "Content": "<email_content>",
        "Attachments": [<attachments>]
    }
    ```

### Filter Emails by Sender
- **Method:** GET
- **Description:** Filter emails by sender email address.
- **Path Parameter:**
    - `sender`: Email address of the sender to filter emails by.
- **Response:**
    ```json
    [<filtered_email_details>]
    ```

### Filter Emails by Subject
- **Method:** GET
- **Description:** Filter emails by subject keyword.
- **Path Parameter:**
    - `keyword`: Keyword to filter emails by subject.
- **Response:**
    ```json
    [<filtered_email_details>]
    ```

### Filter Emails by Importance
- **Method:** GET
- **Description:** Filter emails by importance level.
- **Path Parameter:**
    - `level`: Importance level to filter emails by.
- **Response:**
    ```json
    [<filtered_email_details>]
    ```

### Initialize AI Models
- **Method:** POST
- **Description:** Initialize the AI models for text summarization, tag generation, and spam detection.
- **Response:**
    ```json
    {
        "success": true/false,
        "message": "<success/error_message>"
    }
    ```

### Summarize Text
- **Method:** POST
- **Description:** Generate a summary of the provided text using AI text summarization models.
- **Request Body:**
    ```json
    {
        "text": "<text_to_summarize>"
    }
    ```
- **Response:**
    ```json
    {
        "summary": "<generated_summary>"
    }
    ```

### Get Tags for Text
- **Method:** POST
- **Description:** Retrieve tags for the provided text using AI tag generation models.
- **Request Body:**
    ```json
    {
        "text": "<text_to_get_tags_for>"
    }
    ```
- **Response:**
    ```json
    {
        "tags": ["tag1", "tag2", ...]
    }
    ```

### Detect Spam in Text
- **Method:** POST
- **Description:** Detect spam in the provided text using AI spam detection models.
- **Request Body:**
    ```json
    {
        "text": "<text_to_detect_spam_in>"
    }
    ```
- **Response:**
    ```json
    {
        "spam": true/false
    }
    ```
