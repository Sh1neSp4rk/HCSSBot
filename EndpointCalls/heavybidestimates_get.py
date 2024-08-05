import requests
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, log_process_start, log_process_completion, log_error

# Set up the main logger
logger = setup_main_logger()

def get_HeavyBidEstimates_business_units():
    url = "https://api.hcssapps.com/heavybidestimates/api/v1/BusinessUnits"
    token = get_token()
    if not token:
        log_error(logger, "Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_process_start(logger, "get_HeavyBidEstimates_business_units")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Response code for heavy bid estimates business units: {response.status_code}")

        data = response.json()
        return data
    except requests.RequestException as e:
        log_error(logger, f"Error fetching heavy bid estimates business units: {e}")
        return None
    finally:
        log_process_completion(logger, "get_HeavyBidEstimates_business_units", start_time)

def get_HeavyBidEstimates_partitions():
    url = "https://api.hcssapps.com/heavybidestimates/api/v1/Partitions"
    token = get_token()
    if not token:
        log_error(logger, "Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_process_start(logger, "get_HeavyBidEstimates_partitions")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Response code for heavy bid estimates partitions: {response.status_code}")

        data = response.json()
        return data
    except requests.RequestException as e:
        log_error(logger, f"Error fetching heavy bid estimates partitions: {e}")
        return None
    finally:
        log_process_completion(logger, "get_HeavyBidEstimates_partitions", start_time)
