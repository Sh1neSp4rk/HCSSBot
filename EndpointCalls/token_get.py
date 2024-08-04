# EndpointCalls/token_get.py
import logging
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_token():
    url = "https://api.hcssapps.com/identity/connect/token"
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    grant_type = os.getenv('GRANT_TYPE')
    scope = os.getenv('SCOPE')

    if not client_id or not client_secret or not grant_type or not scope:
        logging.error("One or more environment variables are not set")
        return None

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "scope": scope,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            return data.get('access_token')
        except ValueError as e:
            logging.error("Error decoding JSON:", e)
            logging.error("Response content:", response.text)
            return None
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        logging.error("Response content:", response.text)
        return None
