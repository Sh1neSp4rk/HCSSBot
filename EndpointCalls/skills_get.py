# EndpointCalls/skills_get.py
import logging
import requests
import re
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

def get_last_successful_date(function_name):
    try:
        with open('Logs/data_fetch.log', 'r') as log_file:
            logs = log_file.readlines()
        
        # Reverse logs to start searching from the end
        logs.reverse()
        
        pattern = rf"{function_name} completed at (\S+)"
        for log in logs:
            match = re.search(pattern, log)
            if match:
                return match.group(1)
    
    except FileNotFoundError:
        logging.error("Log file not found.")
    except Exception as e:
        logging.error(f"Error retrieving last successful date: {e}")
    
    return None

def get_Skills_skills(offset=0, forceall=False):
    url = "https://api.hcssapps.com/skills/api/v1/skills"
    date_after_utc = get_last_successful_date("get_Skills_skills") if not forceall else None
    query = {
        "limit": "1000",
        "offset": offset
    }
    if date_after_utc:
        query["dateAfterUtc"] = date_after_utc

    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("get_Skills_skills")
    logging.info(f"Fetching skills with offset: {offset}, dateAfterUtc: {date_after_utc}")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for skills: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching skills: {response.status_code}")
        log_function_completion("get_Skills_skills", start_time)
        return None

    data = response.json()
    log_function_completion("get_Skills_skills", start_time)
    return data

def get_Skills_employeeskills(offset=0, forceall=False):
    url = "https://api.hcssapps.com/skills/api/v1/employeeSkills"
    date_after_utc = get_last_successful_date("get_Skills_employeeskills") if not forceall else None
    query = {
        "limit": "1000",
        "offset": offset,
        "includeDismissed": "true",
        "usePayrollCode": "true"
    }
    if date_after_utc:
        query["dateAfterUtc"] = date_after_utc

    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("get_Skills_employeeskills")
    logging.info(f"Fetching employee skills with offset: {offset}, dateAfterUtc: {date_after_utc}")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for employee skills: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching employee skills: {response.status_code}")
        log_function_completion("get_Skills_employeeskills", start_time)
        return None

    data = response.json()
    log_function_completion("get_Skills_employeeskills", start_time)
    return data
