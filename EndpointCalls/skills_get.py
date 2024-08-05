# EndpointCalls/skills_get.py
import requests
import re
from datetime import datetime
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, log_process_start, log_process_completion, log_error

# Set up the main logger
logger = setup_main_logger()

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
        log_error(logger, "Log file not found.")
    except Exception as e:
        log_error(logger, f"Error retrieving last successful date: {e}")
    
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
        log_error(logger, "Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_process_start(logger, "get_Skills_skills")
    try:
        logger.info(f"Fetching skills with offset: {offset}, dateAfterUtc: {date_after_utc}")
        response = requests.get(url, headers=headers, params=query)
        logger.info(f"Response code for skills: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching skills: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    except ValueError as e:
        log_error(logger, "Error decoding JSON response", exc_info=e)
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Skills_skills", start_time)

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
        log_error(logger, "Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_process_start(logger, "get_Skills_employeeskills")
    try:
        logger.info(f"Fetching employee skills with offset: {offset}, dateAfterUtc: {date_after_utc}")
        response = requests.get(url, headers=headers, params=query)
        logger.info(f"Response code for employee skills: {response.status_code}")

        if response.status_code != 200:
            log_error(logger, f"Error fetching employee skills: {response.status_code}")
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log_error(logger, f"Request failed: {e}")
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    except ValueError as e:
        log_error(logger, "Error decoding JSON response", exc_info=e)
        log_error(logger, f"Response content: {response.text if response else 'No response content'}")
        return None
    finally:
        log_process_completion(logger, "get_Skills_employeeskills", start_time)
