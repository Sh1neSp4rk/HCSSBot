# EndpointCalls/users_users.py
import logging
from EndpointCalls.token_get import get_token
from Tools.progress_bars import fetch_paginated_data_with_progress

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_all_users(business_unit_id, page_size=50):
    endpoint = "https://api.hcssapps.com/users/api/v1/Users"
    logging.info(f"Fetching users for business unit ID: {business_unit_id} with page size: {page_size}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_paginated_data_with_progress(endpoint, headers, business_unit_id, page_size)
