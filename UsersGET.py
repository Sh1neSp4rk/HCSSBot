# UsersGET.py
import logging
from TokenGET import get_token
from ProgressBars import fetch_data_with_progress, fetch_paginated_data_with_progress
from DataSaver import save_data

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

def get_jobs(business_unit_id):
    endpoint = "https://api.hcssapps.com/users/api/v1/Jobs/GetJobsByBusinessUnit"
    params = {"businessUnitId": business_unit_id}
    logging.info(f"Fetching jobs for business unit ID: {business_unit_id} from {endpoint}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_data_with_progress(endpoint, headers, params).json()

def get_roles():
    endpoint = "https://api.hcssapps.com/users/api/v1/Roles"
    logging.info(f"Fetching roles from {endpoint}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_data_with_progress(endpoint, headers).json()

def get_subscription_groups():
    endpoint = "https://api.hcssapps.com/users/api/v1/SubscriptionGroups"
    logging.info(f"Fetching subscription groups from {endpoint}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_data_with_progress(endpoint, headers).json()

def get_all_users(business_unit_id, page_size=50):
    endpoint = "https://api.hcssapps.com/users/api/v1/Users"
    logging.info(f"Fetching users for business unit ID: {business_unit_id} with page size: {page_size}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_paginated_data_with_progress(endpoint, headers, business_unit_id, page_size)

if __name__ == "__main__":
    logging.info("Starting data fetch process")
    business_units = get_business_units()
    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        roles = get_roles()
        if roles:
            logging.info(f"Fetched roles: {roles}")
            save_data(roles, 'roles_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed

        subscription_groups = get_subscription_groups()
        if subscription_groups:
            logging.info(f"Fetched subscription groups: {subscription_groups}")
            save_data(subscription_groups, 'subscription_groups_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed

        jobs = get_jobs(business_unit_id)
        if jobs:
            logging.info(f"Fetched jobs: {jobs}")
            save_data(jobs, 'jobs_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed

        users = get_all_users(business_unit_id)
        if users:
            logging.info(f"Fetched users: {users}")
            save_data(users, 'users_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed
    else:
        logging.error("No business units found")
