# EndpointCalls/token_get.py
import os
import requests
from dotenv import load_dotenv
from Tools.logger import setup_main_logger, log_error, log_process_start, log_process_completion

# Load environment variables
load_dotenv()

# Set up the main logger
logger = setup_main_logger()

def get_token():
    url = "https://api.hcssapps.com/identity/connect/token"
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    grant_type = os.getenv('GRANT_TYPE')
    scope = os.getenv('SCOPE')

    if not client_id or not client_secret or not grant_type or not scope:
        log_error(logger, "One or more environment variables (CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, SCOPE) are not set.")
        return None

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "scope": scope,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    log_process_start(logger, "Requesting token")
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()
        access_token = data.get('access_token')

        if access_token:
            logger.info("Token successfully retrieved.")
        else:
            log_error(logger, "Access token not found in the response.")

        log_process_completion(logger, "Token request")
        return access_token

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    except ValueError as e:
        log_error(logger, "Error decoding JSON response", exc_info=e)
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
