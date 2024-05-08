import os
import random
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

# Define API URLs and headers
API_URLS = {
    "Summarizer": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
    "Detector": "https://api-inference.huggingface.co/models/h-e-l-l-o/email-spam-classification-merged",
    "Tagger": "https://api-inference.huggingface.co/models/fabiochiu/t5-base-tag-generation"
}
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

async def make_api_request(session, url, payload):
    """
    Makes an asynchronous API request using aiohttp.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        url (str): The URL to make the request to.
        payload (dict): The payload to include in the request.

    Returns:
        dict: The JSON response from the API, or None if an error occurs.
    """
    try:
        async with session.post(url, headers=HEADERS, json=payload) as response:
            response = await response.json()
            return response
    except aiohttp.ClientError as e:
        print(f"Error occurred while making request: {e}")
        return None

async def initialize_models(session):
    """
    Initializes the models by making asynchronous API requests to check their status.
    
    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
    """
    async def initialize_model(model_name, model_url):
        """
        Initializes a single model by making asynchronous API requests to check its status.

        Args:
            model_name (str): The name of the model.
            model_url (str): The URL of the model's API endpoint.
        """
        retries = 0
        max_retries = 5
        while retries < max_retries:
            response = await make_api_request(session, model_url, {"inputs": "Hello, World!"})
            if isinstance(response, dict) and 'error' in response and 'estimated_time' in response:
                estimated_time = response['estimated_time']
                print(f"Model {model_name} is currently loading. Waiting for {estimated_time} seconds...")
                await asyncio.sleep(estimated_time + random.uniform(0, 1) * 0.1)  # Add small jitter
                retries += 1
            else:
                print(f"{model_name} initialized successfully")
                return
        print(f"Failed to initialize {model_name} after {max_retries} retries")
    
    tasks = [initialize_model(model_name, model_url) for model_name, model_url in API_URLS.items()]
    await asyncio.gather(*tasks)

async def summarize_text(text, session):
    """
    Summarizes the given text using the Summarizer API.

    Args:
        text (str): The text to be summarized.
        session (aiohttp.ClientSession): The aiohttp client session.

    Returns:
        dict: The summary response from the API.
    """
    payload = {
        "inputs": text,
        "parameters": {
            "max_new_tokens": 100,
            "do_sample": False,
            "max_length": 100,
            "min_length": 10
        }
    }
    return await make_api_request(session, API_URLS["Summarizer"], payload)

async def detect_spam(text, session):
    """
    Detects spam in the given text using the Detector API.

    Args:
        text (str): The text to be analyzed for spam.
        session (aiohttp.ClientSession): The aiohttp client session.

    Returns:
        dict: The spam detection response from the API.
    """
    payload = {
        "inputs": text,
        "parameters": {}
    }
    return await make_api_request(session, API_URLS["Detector"], payload)

async def get_tags(text, session):
    """
    Retrieves tags for the given text using the Tagger API.

    Args:
        text (str): The text to be analyzed for tags.
        session (aiohttp.ClientSession): The aiohttp client session.

    Returns:
        dict: The tags response from the API.
    """
    payload = {
        "inputs": text,
        "parameters": {
            "max_new_tokens": 100,
            "do_sample": True,
            "max_length": 100,
            "min_length": 10,
            "num_beams": 8,
        }
    }
    return await make_api_request(session, API_URLS["Tagger"], payload)

if __name__ == "__main__":
    
    async def main():
        async with aiohttp.ClientSession() as session:
            await initialize_models(session)

            # Example text for testing the APIs
            text = """
            Subject: Your Amazon.com order cannot be shipped
            
            Dear Customer,
            Greetings from Amazon.com.
            We're writing to inform you that your order cannot be shipped.
            We're sorry for any inconvenience this may cause.
            We'll refund your order in full.
            Thank you for shopping with us.
            
            Best regards,
            Amazon.com Customer Service
            """
            summary = await summarize_text(text, session)
            spam = await detect_spam(text, session)
            tags = await get_tags(text, session)

            print("Summary:", summary)
            print("Spam Detection:", spam)
            print("Tags:", tags)
            
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
