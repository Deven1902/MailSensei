import os
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

API_URLS = {
    "Summarizer": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
    "Detector": "https://api-inference.huggingface.co/models/h-e-l-l-o/email-spam-classification-merged",
    "Tagger": "https://api-inference.huggingface.co/models/fabiochiu/t5-base-tag-generation"
}

HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

async def make_api_request(session, url, payload):
    try:
        async with session.post(url, headers=HEADERS, json=payload) as response:
            response = await response.json()
            return response
    except aiohttp.ClientError as e:
        print(f"Error occurred while making request: {e}")
        return None

async def initialize_models(session):
    tasks = [make_api_request(session, url, {"inputs": "Hello, World!"}) for url in API_URLS.values()]
    responses = await asyncio.gather(*tasks)

    for model_name, response in zip(API_URLS.keys(), responses):
        if response is None:
            print(f"Error occurred while initializing {model_name.lower()}")
        else:
            print(f"{model_name} initialized successfully")

async def summarize_text(text, session):
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
    payload = {
        "inputs": text,
        "parameters": {}
    }
    return await make_api_request(session, API_URLS["Detector"], payload)

async def get_tags(text, session):
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
