# EndpointCalls/users_get.py
from Tools.logger import setup_main_logger, log_error, log_process_start, log_process_completion
from Tools.progress_bars import fetch_data_with_progress, fetch_paginated_data_with_progress
from EndpointCalls.token_get import get_token

# Set up logging
logger = setup_main_logger()

def get_headers():
    token = get_token()
    if not token:
        log_error(logger, "Failed to retrieve token")
        return None
    return {"Authorization": f"Bearer {token}"}

def get_Users_business_units():
    endpoint = "https://api.hcssapps.com/users/api/v1/BusinessUnits"
    log_process_start(logger, "Fetching business units")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers)
    if response.status_code == 200:
        result = response.json().get('results', [])
        log_process_completion(logger, "Fetching business units")
        return result
    else:
        log_error(logger, f"Error fetching business units: {response.status_code}")
        return None

def get_Users_jobs(business_unit_id=None):
    if business_unit_id is None:
        business_units = get_Users_business_units()
        if not business_units:
            log_error(logger, "No business units found.")
            return None
        all_jobs = []
        for unit in business_units:
            unit_id = unit.get('id')
            if unit_id:
                jobs = get_Users_jobs(business_unit_id=unit_id)
                if jobs:
                    all_jobs.extend(jobs)
        return all_jobs

    endpoint = "https://api.hcssapps.com/users/api/v1/Jobs/GetJobsByBusinessUnit"
    params = {"businessUnitId": business_unit_id}
    log_process_start(logger, f"Fetching jobs for business unit ID: {business_unit_id}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers, params)
    if response.status_code == 200:
        result = response.json().get('results', [])
        log_process_completion(logger, f"Fetching jobs for business unit ID: {business_unit_id}")
        return result
    else:
        log_error(logger, f"Error fetching jobs: {response.status_code}")
        return None

def get_Users_roles():
    endpoint = "https://api.hcssapps.com/users/api/v1/Roles"
    log_process_start(logger, "Fetching roles")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers)
    if response.status_code == 200:
        result = response.json().get('results', [])
        log_process_completion(logger, "Fetching roles")
        return result
    else:
        log_error(logger, f"Error fetching roles: {response.status_code}")
        return None

def get_Users_subscription_groups():
    endpoint = "https://api.hcssapps.com/users/api/v1/SubscriptionGroups"
    log_process_start(logger, "Fetching subscription groups")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers)
    if response.status_code == 200:
        result = response.json().get('results', [])
        log_process_completion(logger, "Fetching subscription groups")
        return result
    else:
        log_error(logger, f"Error fetching subscription groups: {response.status_code}")
        return None

def fetch_users_for_business_unit(business_unit_id, page_size, offset):
    endpoint = "https://api.hcssapps.com/users/api/v1/Users"
    params = {
        "businessUnitId": business_unit_id,
        "pageSize": page_size,
        "offset": offset
    }
    log_process_start(logger, f"Fetching users for business unit ID: {business_unit_id} with offset {offset}")
    headers = get_headers()
    if headers is None:
        return None
    response = fetch_data_with_progress(endpoint, headers, params)
    if response.status_code == 200:
        return response.json()
    else:
        log_error(logger, f"Error fetching users: {response.status_code}")
        return None

def get_Users_users(business_unit_id=None, page_size=50, all_users=None):
    if all_users is None:
        all_users = []

    if business_unit_id is None:
        business_units = get_Users_business_units()
        if not business_units:
            log_error(logger, "No business units found.")
            return None
        for unit in business_units:
            unit_id = unit.get('id')
            if unit_id:
                get_Users_users(business_unit_id=unit_id, page_size=page_size, all_users=all_users)
        return all_users

    offset = 0
    log_process_start(logger, f"Fetching users for business unit ID: {business_unit_id}")
    while True:
        response = fetch_users_for_business_unit(business_unit_id, page_size, offset)
        if not response or not response.get('users'):
            break
        users = response.get('users')
        all_users.extend(users)
        offset += page_size
        logger.info(f"Fetched {len(users)} users from business unit {business_unit_id}, offset {offset}")

    log_process_completion(logger, f"Fetching users for business unit ID: {business_unit_id}")
    return all_users
