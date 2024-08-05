# EndpointCalls/users_get.py
import logging
from Tools.progress_bars import fetch_data_with_progress, fetch_paginated_data_with_progress
from EndpointCalls.token_get import get_token

# Configure logging
logging.basicConfig(
    filename='Logs/users_fetch.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_headers():
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    return {"Authorization": f"Bearer {token}"}

def get_business_units():
    endpoint = "https://api.hcssapps.com/users/api/v1/BusinessUnits"
    logging.info(f"Fetching business units from {endpoint}")
    headers = get_headers()
    if headers is None:
        return
    response = fetch_data_with_progress(endpoint, headers)
    logging.info(f"Response code for business units: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Error fetching business units: {response.status_code}")

def get_jobs(business_unit_id):
    endpoint = "https://api.hcssapps.com/users/api/v1/Jobs/GetJobsByBusinessUnit"
    params = {"businessUnitId": business_unit_id}
    logging.info(f"Fetching jobs for business unit ID: {business_unit_id} from {endpoint}")
    headers = get_headers()
    if headers is None:
        return
    response = fetch_data_with_progress(endpoint, headers, params)
    logging.info(f"Response code for jobs: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Error fetching jobs: {response.status_code}")

def get_roles():
    endpoint = "https://api.hcssapps.com/users/api/v1/Roles"
    logging.info(f"Fetching roles from {endpoint}")
    headers = get_headers()
    if headers is None:
        return
    response = fetch_data_with_progress(endpoint, headers)
    logging.info(f"Response code for roles: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Error fetching roles: {response.status_code}")

def get_subscription_groups():
    endpoint = "https://api.hcssapps.com/users/api/v1/SubscriptionGroups"
    logging.info(f"Fetching subscription groups from {endpoint}")
    headers = get_headers()
    if headers is None:
        return
    response = fetch_data_with_progress(endpoint, headers)
    logging.info(f"Response code for subscription groups: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Error fetching subscription groups: {response.status_code}")

def get_all_users(business_unit_id, page_size=50):
    endpoint = "https://api.hcssapps.com/users/api/v1/Users"
    logging.info(f"Fetching users for business unit ID: {business_unit_id} with page size: {page_size}")
    headers = get_headers()
    if headers is None:
        return
    response = fetch_paginated_data_with_progress(endpoint, headers, business_unit_id, page_size)
    logging.info(f"Response code for users: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Error fetching users: {response.status_code}")
