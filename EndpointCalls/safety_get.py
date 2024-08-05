# EndpointCalls/safety_get.py
import logging
import requests
from EndpointCalls.token_get import get_token
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='Logs/safety_get.log',
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

def get_safety_data():
    url = "https://api.hcssapps.com/safety/api/v1/data"
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("get_safety_data")
    response = requests.get(url, headers=headers)
    logging.info(f"Response code for safety data: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching safety data: {response.status_code}")
        log_function_completion("get_safety_data", start_time)
        return None

    data = response.json()
    log_function_completion("get_safety_data", start_time)
    return data
