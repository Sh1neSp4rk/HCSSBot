# EndpointCalls/telematics_get.py
from datetime import datetime
import requests
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, log_process_start, log_process_completion, log_error
from Tools.progress_bars import fetch_paginated_data_with_progress

# Set up the main logger
logger = setup_main_logger()

def get_Telematics_equipment(cursor=None):
    url = "https://api.hcssapps.com/telematics/api/v1/equipment"
    query = {
        "limit": "1000",
        "cursor": cursor,
        "isRegistered": "true"
    }

    token = get_token()
    if not token:
        log_error(logger, "Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}

    log_process_start(logger, "Fetching equipment data")
    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        logger.info(f"Response code for equipment data: {response.status_code}")

        data = response.json()
        next_cursor = data.get("metadata", {}).get("nextCursor")

        if next_cursor:
            logger.info(f"Next cursor found: {next_cursor}")
            results = data.get("results", [])
            results.extend(get_Telematics_equipment(cursor=next_cursor) or [])
        else:
            results = data.get("results", [])

        log_process_completion(logger, "Fetching equipment data")
        return results

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        log_process_completion(logger, "Fetching equipment data")
        return None
    except ValueError as e:
        log_error(logger, "Error decoding JSON response", exc_info=e)
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        log_process_completion(logger, "Fetching equipment data")
        return None
