import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

# Set the API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# GPT-3.5 TURBO CONFIGURATION
client = OpenAI(api_key=OPENAI_API_KEY)
msgs = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=msgs
)

def call_gpt_3_5_with_context(user_query: str) -> str:
    """
    Calls the GPT-3.5 Turbo model to generate a response based on the user query.

    Args:
        user_query (str): The user's query.

    Returns:
        str: The generated response.
    """
    try:
        msgs.append({"role": "user", "content": user_query})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=msgs
        )
        msgs.append({"role": "system", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    except Exception as e:
        # Handle the error here
        print(f"An error occurred: {e}")
        return ""

def call_gpt_3_5_without_context(user_query: str) -> str:
    """
    Calls the GPT-3.5 Turbo model to generate a response based on the user query.

    Args:
        user_query (str): The user's query.

    Returns:
        str: The generated response.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_query,
                }
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Handle the error here
        print(f"An error occurred: {e}")
        return "" 
    
# GEMINI PRO CONFIGURATION
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
gemini_chat_session = model.start_chat(history=[])

def call_gemini_pro_with_context(user_query: str) -> str:
    """
    Calls the Gemini Pro model to generate a response based on the user query.

    Args:
        user_query (str): The user's query.

    Returns:
        str: The generated response.
    """
    try:
        response = gemini_chat_session.send_message(user_query)
        return response.text
    except Exception as e:
        # Handle the error here
        print(f"An error occurred: {e}")
        return ""

def call_gemini_pro_without_context(user_query: str) -> str:
    """
    Calls the Gemini Pro model to generate a response based on the user query.

    Args:
        user_query (str): The user's query.

    Returns:
        str: The generated response.
    """
    try:
        response = model.generate_content(user_query)
        return response.text
    except Exception as e:
        # Handle the error here
        print(f"An error occurred: {e}")
        return ""
    