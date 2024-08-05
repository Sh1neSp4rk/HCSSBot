# EndpointCalls/setups_get.py
import logging
import requests
from EndpointCalls.token_get import get_token
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='Logs/setups_get.log',
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

def get_headers():
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    return {"Authorization": f"Bearer {token}"}

def get_Setups_business_units():
    url = "https://api.hcssapps.com/setups/api/v1/BusinessUnit"
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_function_call("get_business_units")
    response = requests.get(url, headers=headers)
    logging.info(f"Response code for business units: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching business units: {response.status_code}")
        log_function_completion("get_business_units", start_time)
        return None

    data = response.json()
    log_function_completion("get_business_units", start_time)
    return data

def get_Setups_accounting_templates(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            logging.error("No business units found.")
            return None
        all_templates = []
        for unit in business_units:
            unit_code = unit.get('code')
            if unit_code:
                templates = get_Setups_accounting_templates(business_unit_code=unit_code)
                if templates:
                    all_templates.extend(templates)
        return all_templates

    url = "https://api.hcssapps.com/setups/api/v1/AccountingTemplate"
    query = {"businessUnitCode": business_unit_code}
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_function_call("get_Setups_accounting_templates")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for accounting templates: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching accounting templates: {response.status_code}")
        log_function_completion("get_Setups_accounting_templates", start_time)
        return None

    data = response.json()
    log_function_completion("get_Setups_accounting_templates", start_time)
    return data

def get_Setups_jobs(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            logging.error("No business units found.")
            return None
        all_jobs = []
        for unit in business_units:
            unit_code = unit.get('code')
            if unit_code:
                jobs = get_Setups_jobs(business_unit_code=unit_code)
                if jobs:
                    all_jobs.extend(jobs)
        return all_jobs

    url = "https://api.hcssapps.com/setups/api/v1/Job"
    query = {
        "businessUnitCode": business_unit_code,
    }
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_function_call("get_Setups_jobs")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for jobs: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching jobs: {response.status_code}")
        log_function_completion("get_Setups_jobs", start_time)
        return None

    data = response.json()
    log_function_completion("get_Setups_jobs", start_time)
    return data

def get_Setups_equipment(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            logging.error("No business units found.")
            return None
        all_equipment = []
        for unit in business_units:
            unit_code = unit.get('code')
            if unit_code:
                equipment = get_Setups_equipment(business_unit_code=unit_code)
                if equipment:
                    all_equipment.extend(equipment)
        return all_equipment

    url = "https://api.hcssapps.com/setups/api/v1/Equipment"
    query = {
        "businessUnitCode": business_unit_code,
    }
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_function_call("get_Setups_equipment")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for equipment: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching equipment: {response.status_code}")
        log_function_completion("get_Setups_equipment", start_time)
        return None

    data = response.json()
    log_function_completion("get_Setups_equipment", start_time)
    return data

def get_Setups_employees(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            logging.error("No business units found.")
            return None
        all_employees = []
        for unit in business_units:
            unit_code = unit.get('code')
            if unit_code:
                employees = get_Setups_employees(business_unit_code=unit_code)
                if employees:
                    all_employees.extend(employees)
        return all_employees

    url = "https://api.hcssapps.com/setups/api/v1/Employee"
    query = {
        "businessUnitCode": business_unit_code,
    }
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_function_call("get_Setups_employees")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for employees: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching employees: {response.status_code}")
        log_function_completion("get_Setups_employees", start_time)
        return None

    data = response.json()
    log_function_completion("get_Setups_employees", start_time)
    return data
