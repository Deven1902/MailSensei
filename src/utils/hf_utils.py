import os
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

class APIConfig:
    SUMMARIZER_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    DETECTOR_API_URL = "https://api-inference.huggingface.co/models/1aurent/distilbert-base-multilingual-cased-finetuned-email-spam"
    TAGGER_API_URL = "https://api-inference.huggingface.co/models/fabiochiu/t5-base-tag-generation"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename='llm.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def initialize_models():
    models = {
        "Summarizer": APIConfig.SUMMARIZER_API_URL,
        "Detector": APIConfig.DETECTOR_API_URL,
        "Tagger": APIConfig.TAGGER_API_URL
    }

    with requests.Session() as session:
        for model_name, model_url in models.items():
            try:
                response = session.get(model_url)
                response = response.json()
                print(response)
                logging.info(f"{model_name} model status: {response['status']}")
            except requests.RequestException as e:
                logging.error(f"Error occurred while initializing {model_name.lower()}: {str(e)}")
                return None

def make_api_request(url, payload):
    try:
        with requests.Session() as session:
            response = session.post(url, headers=APIConfig.headers, json=payload)
            response = response.json()
            return response
    except requests.RequestException as e:
        logging.error(f"Error occurred during API request: {str(e)}")
        return None

def summarize_text(text):
    payload = {"inputs": text}
    return make_api_request(APIConfig.SUMMARIZER_API_URL, payload)

def detect_spam(text):
    payload = {"inputs": text}
    return make_api_request(APIConfig.DETECTOR_API_URL, payload)

def get_tags(text):
    payload = {"inputs": text}
    return make_api_request(APIConfig.TAGGER_API_URL, payload)

if __name__ == "__main__":
    configure_logging()
    initialize_models()

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
    print(summarize_text(text))
    print(detect_spam(text))
    print(get_tags(text))
