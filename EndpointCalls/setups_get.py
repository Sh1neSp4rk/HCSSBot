# EndpointCalls/setups_get.py
import requests
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, log_process_start, log_process_completion, log_error

# Set up the main logger
logger = setup_main_logger()

def get_headers():
    token = get_token()
    if not token:
        log_error(logger, "Failed to retrieve token")
        return None
    return {"Authorization": f"Bearer {token}"}

def get_Setups_business_units():
    url = "https://api.hcssapps.com/setups/api/v1/BusinessUnit"
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_process_start(logger, "get_Setups_business_units")
    try:
        response = requests.get(url, headers=headers)
        logger.info(f"Response code for business units: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching business units: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Setups_business_units", start_time)

def get_Setups_accounting_templates(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            log_error(logger, "No business units found.")
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
    
    start_time = log_process_start(logger, "get_Setups_accounting_templates")
    try:
        response = requests.get(url, headers=headers, params=query)
        logger.info(f"Response code for accounting templates: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching accounting templates: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Setups_accounting_templates", start_time)

def get_Setups_jobs(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            log_error(logger, "No business units found.")
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
    query = {"businessUnitCode": business_unit_code}
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_process_start(logger, "get_Setups_jobs")
    try:
        response = requests.get(url, headers=headers, params=query)
        logger.info(f"Response code for jobs: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching jobs: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Setups_jobs", start_time)

def get_Setups_equipment(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            log_error(logger, "No business units found.")
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
    query = {"businessUnitCode": business_unit_code}
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_process_start(logger, "get_Setups_equipment")
    try:
        response = requests.get(url, headers=headers, params=query)
        logger.info(f"Response code for equipment: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching equipment: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Setups_equipment", start_time)

def get_Setups_employees(business_unit_code=None):
    if business_unit_code is None:
        business_units = get_Setups_business_units()
        if not business_units:
            log_error(logger, "No business units found.")
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
    query = {"businessUnitCode": business_unit_code}
    headers = get_headers()
    if headers is None:
        return None
    
    start_time = log_process_start(logger, "get_Setups_employees")
    try:
        response = requests.get(url, headers=headers, params=query)
        logger.info(f"Response code for employees: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching employees: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Setups_employees", start_time)
