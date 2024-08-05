# EndpointCalls/heavybidestimates_get.py
import logging
import requests
from EndpointCalls.token_get import get_token
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='Logs/heavybidestimates_get.log',
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

def get_HeavyBidEstimates_business_units():
    url = "https://api.hcssapps.com/heavybidestimates/api/v1/BusinessUnits"
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("get_heavybidestimates_business_units")
    response = requests.get(url, headers=headers)
    logging.info(f"Response code for heavy bid estimates business units: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching heavy bid estimates business units: {response.status_code}")
        log_function_completion("get_heavybidestimates_business_units", start_time)
        return None

    data = response.json()
    log_function_completion("get_heavybidestimates_business_units", start_time)
    return data

def get_HeavyBidEstimates_partitions():
    url = "https://api.hcssapps.com/heavybidestimates/api/v1/Partitions"
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("get_heavybidestimates_partitions")
    response = requests.get(url, headers=headers)
    logging.info(f"Response code for heavy bid estimates partitions: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching heavy bid estimates partitions: {response.status_code}")
        log_function_completion("get_heavybidestimates_partitions", start_time)
        return None

    data = response.json()
    log_function_completion("get_heavybidestimates_partitions", start_time)
    return data