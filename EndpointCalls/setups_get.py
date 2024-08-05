# EndpointCalls/setups_get.py
import logging
import requests
from EndpointCalls.token_get import get_token
from datetime import datetime
from Tools.progress_bars import fetch_data_with_progress

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

def fetch_accounting_templates(business_unit_code):
    url = "https://api.hcssapps.com/setups/api/v1/AccountingTemplate"
    query = {
        "businessUnitCode": business_unit_code
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_accounting_templates")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for accounting templates: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching accounting templates: {response.status_code}")
        log_function_completion("fetch_accounting_templates", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_accounting_templates", start_time)
    return data

def fetch_business_units():
    url = "https://api.hcssapps.com/setups/api/v1/BusinessUnit"
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_business_units")
    response = requests.get(url, headers=headers)
    logging.info(f"Response code for business units: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching business units: {response.status_code}")
        log_function_completion("fetch_business_units", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_business_units", start_time)
    return data

def fetch_jobs(business_unit_code, accounting_template_name=""):
    url = "https://api.hcssapps.com/setups/api/v1/Job"
    query = {
        "businessUnitCode": business_unit_code,
        "accountingTemplateName": accounting_template_name
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_jobs")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for jobs: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching jobs: {response.status_code}")
        log_function_completion("fetch_jobs", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_jobs", start_time)
    return data

def fetch_equipment(business_unit_code, accounting_template_name=""):
    url = "https://api.hcssapps.com/setups/api/v1/Equipment"
    query = {
        "businessUnitCode": business_unit_code,
        "accountingTemplateName": accounting_template_name
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_equipment")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for equipment: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching equipment: {response.status_code}")
        log_function_completion("fetch_equipment", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_equipment", start_time)
    return data

def fetch_employees(business_unit_code, accounting_template_name="", include_deleted=False):
    url = "https://api.hcssapps.com/setups/api/v1/Employee"
    query = {
        "businessUnitCode": business_unit_code,
        "accountingTemplateName": accounting_template_name,
        "includeDeleted": str(include_deleted).lower()
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_employees")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for employees: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching employees: {response.status_code}")
        log_function_completion("fetch_employees", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_employees", start_time)
    return data
