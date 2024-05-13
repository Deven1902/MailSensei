from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from src.utils.email_utils import GmailClient, strip_tags
from fastapi.middleware.cors import CORSMiddleware
from src.utils.hf_utils import (
    summarize_text,
    get_tags,
    detect_spam,
    initialize_models
)

app = FastAPI()

origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

# Initialize GmailClient object
gmail_client = None

# Define request models
class GmailCredentials(BaseModel):
    gmail_address: str
    app_password: str

class EmailData(BaseModel):
    username: str
    password: str

class TextData(BaseModel):
    text: str

# API Endpoints
@app.post("/setup_gmail_credentials")
async def setup_gmail_credentials(credentials: GmailCredentials):
    # You can securely store the credentials in your backend for future use
    # For demonstration purposes, we are not storing the credentials here
    return {
        "success": True,
        "message": "Gmail credentials setup successful"
    }

@app.post("/connect_gmail")
async def connect_gmail(data: EmailData):
    global gmail_client
    gmail_client = GmailClient(data.username, data.password)
    if await gmail_client.connect():
        return {
            "success": True,
            "message": "Connected to Gmail IMAP server"
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to Gmail IMAP server")

@app.get("/fetch_unread_emails")
async def fetch_unread_emails():
    if not gmail_client:
        raise HTTPException(status_code=400, detail="Gmail client not initialized")
    
    unread_email_ids = await gmail_client.fetch_unread_email_ids()
    if unread_email_ids:
        return {
            "success": True,
            "email_ids": unread_email_ids,
            "message": "Unread email IDs fetched successfully"
        }
    else:
        return {
            "success": True,
            "email_ids": [],
            "message": "No unread emails found"
            }
    
@app.get("/fetch_email_details/{email_id}")
async def fetch_email_details(email_id: int):
    if not gmail_client:
        raise HTTPException(status_code=400, detail="Gmail client not initialized")
    
    email_details = await gmail_client.fetch_email(email_id)
    if email_details and 'Content' in email_details:
        email_details['Content'] = strip_tags(email_details['Content'])
    if email_details:
        return {
            "success": True,
            "email_details": email_details,
            "message": "Email details fetched successfully"
            }
    else:
        return {
            "success": False,
            "email_details": None,
            "message": "Failed to fetch email details"
            }

@app.post("/summarize_text")
async def summarize_text_api(data: TextData):
    summary = await summarize_text(data.text)
    return {
        "success": True,
        "result": summary,
        "message": "Text summarized successfully"
        }

@app.post("/get_tags")
async def get_tags_api(data: TextData):
    tags_result = await get_tags(data.text)
    return {
        "success": True,
        "result": tags_result,
        "message": "Tags retrieved successfully"
        }

@app.post("/detect_spam")
async def detect_spam_api(data: TextData):
    spam_result = await detect_spam(data.text)
    return {
        "success": True,
        "result": spam_result,
        "message": "Spam detected successfully"
        }

@app.post("/initialize_models")
async def initialize_models_api():
    try:
        await initialize_models()
        return {
            "success": True,
            "message": "Models initialized successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to initialize models: {str(e)}"
            }
    
# Add endpoint for filtering emails by sender
@app.get("/filter_by_sender/{sender}")
async def filter_by_sender(sender: str):
    if not gmail_client:
        raise HTTPException(status_code=400, detail="Gmail client not initialized")
    
    # Implement logic to filter emails by sender
    # Modify the email fetching logic accordingly
    pass

# Add endpoint for filtering emails by subject keywords
@app.get("/filter_by_subject/{keyword}")
async def filter_by_subject(keyword: str):
    if not gmail_client:
        raise HTTPException(status_code=400, detail="Gmail client not initialized")
    
    # Implement logic to filter emails by subject keywords
    # Modify the email fetching logic accordingly
    pass

# Add endpoint for filtering emails by importance level
@app.get("/filter_by_importance/{level}")
async def filter_by_importance(level: str):
    if not gmail_client:
        raise HTTPException(status_code=400, detail="Gmail client not initialized")
    
    # Implement logic to filter emails by importance level
    # Modify the email fetching logic accordingly
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    