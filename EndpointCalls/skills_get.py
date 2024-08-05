# EndpointCalls/skills_get.py
import logging
import requests
from EndpointCalls.token_get import get_token
from datetime import datetime

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

def fetch_skills(offset=0):
    url = "https://api.hcssapps.com/skills/api/v1/skills"
    query = {
        "dateAfterUtc": "2019-08-24T14:15:22Z",
        "limit": "1000",
        "offset": offset
    }

    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_skills")
    logging.info(f"Fetching skills with offset: {offset}")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for skills: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching skills: {response.status_code}")
        log_function_completion("fetch_skills", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_skills", start_time)
    return data

def fetch_employee_skills(offset=0):
    url = "https://api.hcssapps.com/skills/api/v1/employeeSkills"
    query = {
        "dateAfterUtc": "2019-08-24T14:15:22Z",
        "limit": "1000",
        "offset": offset,
        "includeDismissed": "true",
        "usePayrollCode": "true"
    }

    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_employee_skills")
    logging.info(f"Fetching employee skills with offset: {offset}")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for employee skills: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching employee skills: {response.status_code}")
        log_function_completion("fetch_employee_skills", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_employee_skills", start_time)
    return data

def get_all_skills():
    all_skills = []
    offset = 0
    while True:
        data = fetch_skills(offset)
        if not data or not data.get('results'):
            break
        all_skills.extend(data.get('results', []))
        offset += len(data.get('results', []))
    logging.info(f"Fetched total skills count: {len(all_skills)}")
    return all_skills

def get_all_employee_skills():
    all_employee_skills = []
    offset = 0
    while True:
        data = fetch_employee_skills(offset)
        if not data or not data.get('results'):
            break
        all_employee_skills.extend(data.get('results', []))
        offset += len(data.get('results', []))
    logging.info(f"Fetched total employee skills count: {len(all_employee_skills)}")
    return all_employee_skills
