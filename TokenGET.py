# TokenGET.py
from dotenv import load_dotenv
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_token():
    # Load environment variables from .env file
    load_dotenv()

    # Endpoint URL
    url = "https://api.hcssapps.com/identity/connect/token"

    # Fetch environment variables
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    grant_type = os.getenv('GRANT_TYPE')
    scope = os.getenv('SCOPE')

    # Check if environment variables are set
    if not client_id or not client_secret or not grant_type or not scope:
        logging.error("One or more environment variables are not set")
        raise ValueError("One or more environment variables are not set")

    # Prepare payload and headers
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "scope": scope,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Send POST request
    logging.info(f"Sending POST request to {url} with payload {payload}")
    response = requests.post(url, data=payload, headers=headers)

    # Check if the response status code indicates success
    if response.status_code == 200:
        try:
            data = response.json()
            logging.info(f"Received access token: {data.get('access_token')}")
            return data.get('access_token')
        except ValueError as e:
            logging.error(f"Error decoding JSON: {e}")
            logging.debug(f"Response content: {response.text}")
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        logging.debug(f"Response content: {response.text}")

    return None
