# EndpointCalls/telematics_get.py
import logging
import requests
from EndpointCalls.token_get import get_token
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='Logs/data_fetch.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_function_call(function_name):
    start_time = datetime.now()
    logging.info(f"{function_name} started at {start_time.isoformat()}")
    return start_time

def log_function_completion(function_name, start_time):
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"{function_name} completed at {end_time.isoformat()} (Elapsed time: {elapsed_time})")

def get_equipment(cursor=None):
    url = "https://api.hcssapps.com/telematics/api/v1/equipment"
    query = {
        "limit": "1000",
        "cursor": cursor,
        "isRegistered": "true"
    }

    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_equipment_data")
    logging.info(f"Fetching equipment data with cursor: {cursor}")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for equipment data: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching equipment data: {response.status_code}")
        log_function_completion("fetch_equipment_data", start_time)
        return None

    data = response.json()
    next_cursor = data.get("metadata", {}).get("nextCursor")

    if next_cursor:
        logging.info(f"Next cursor found: {next_cursor}")
        results = data.get("results", [])
        results.extend(get_equipment(cursor=next_cursor) or [])
    else:
        results = data.get("results", [])

    log_function_completion("fetch_equipment_data", start_time)
    return results
