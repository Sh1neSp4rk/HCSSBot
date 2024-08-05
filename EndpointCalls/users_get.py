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

def get_Users_business_units():
    endpoint = "https://api.hcssapps.com/users/api/v1/BusinessUnits"
    logging.info(f"Fetching business units from {endpoint}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers)
    logging.info(f"Response code for business units: {response.status_code}")
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        logging.error(f"Error fetching business units: {response.status_code}")
        return None

def get_Users_jobs(business_unit_id=None):
    if business_unit_id is None:
        # Fetch business units if ID is not provided
        business_units = get_Users_business_units()
        if not business_units:
            logging.error("No business units found.")
            return None
        all_jobs = []
        # Iterate over all business units and fetch jobs
        for unit in business_units:
            unit_id = unit.get('id')
            if unit_id:
                jobs = get_Users_jobs(business_unit_id=unit_id)
                if jobs:
                    all_jobs.extend(jobs)
        return all_jobs

    endpoint = "https://api.hcssapps.com/users/api/v1/Jobs/GetJobsByBusinessUnit"
    params = {"businessUnitId": business_unit_id}
    logging.info(f"Fetching jobs for business unit ID: {business_unit_id} from {endpoint}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers, params)
    logging.info(f"Response code for jobs: {response.status_code}")
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        logging.error(f"Error fetching jobs: {response.status_code}")
        return None

def get_Users_roles():
    endpoint = "https://api.hcssapps.com/users/api/v1/Roles"
    logging.info(f"Fetching roles from {endpoint}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers)
    logging.info(f"Response code for roles: {response.status_code}")
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        logging.error(f"Error fetching roles: {response.status_code}")
        return None

def get_Users_subscription_groups():
    endpoint = "https://api.hcssapps.com/users/api/v1/SubscriptionGroups"
    logging.info(f"Fetching subscription groups from {endpoint}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers)
    logging.info(f"Response code for subscription groups: {response.status_code}")
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        logging.error(f"Error fetching subscription groups: {response.status_code}")
        return None

def fetch_users_for_business_unit(business_unit_id, page_size, offset):
    endpoint = f"https://api.hcssapps.com/users/api/v1/Users"
    params = {
        "businessUnitId": business_unit_id,
        "pageSize": page_size,
        "offset": offset
    }
    logging.info(f"Fetching users for business unit ID: {business_unit_id} from {endpoint} with offset {offset}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers, params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching users: {response.status_code}")
        return None

def get_Users_users(business_unit_id=None, page_size=50, all_users=None):
    if all_users is None:
        all_users = []

    # If business_unit_id is not provided, fetch all business units
    if business_unit_id is None:
        business_units = get_Users_business_units()
        if not business_units:
            logging.error("No business units found.")
            return None
        # Iterate over all business units
        for unit in business_units:
            unit_id = unit.get('id')
            if unit_id:
                get_Users_users(business_unit_id=unit_id, page_size=page_size, all_users=all_users)
        return all_users

    # Fetch users for the specific business unit
    offset = 0
    while True:
        response = fetch_users_for_business_unit(business_unit_id, page_size, offset)
        if not response or not response.get('users'):
            break
        users = response.get('users')
        all_users.extend(users)
        offset += page_size
        logging.info(f"Fetched {len(users)} users from business unit {business_unit_id}, offset {offset}")

    return all_users
