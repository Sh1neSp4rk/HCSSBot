# EndpointCalls/users_business_units.py
import logging
from EndpointCalls.token_get import get_token
from Tools.progress_bars import fetch_data_with_progress

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_business_units():
    endpoint = "https://api.hcssapps.com/users/api/v1/BusinessUnits"
    logging.info(f"Fetching business units from {endpoint}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_data_with_progress(endpoint, headers).json()
