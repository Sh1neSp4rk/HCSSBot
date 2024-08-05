# EndpointCalls/safety_get.py
import logging
import requests
from datetime import datetime
from EndpointCalls.token_get import get_token
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

def get_incidents(modified_after_utc=None, created_after_utc=None, incident_date_after_utc=None, incident_date_before_utc=None, limit=0, offset=0):
    url = "https://api.hcssapps.com/safety/v1/incidents"
    query = {
        "modifiedAfterUtc": modified_after_utc,
        "createdAfterUtc": created_after_utc,
        "incidentDateAfterUtc": incident_date_after_utc,
        "incidentDateBeforeUtc": incident_date_before_utc,
        "limit": limit,
        "offset": offset
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_incidents")
    response = fetch_data_with_progress(url, headers, query)
    logging.info(f"Response code for incidents: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching incidents: {response.status_code}")
        log_function_completion("fetch_incidents", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_incidents", start_time)
    return data

def get_incident_details(incident_id, exclude_forms=True):
    url = f"https://api.hcssapps.com/safety/v2/incidents/{incident_id}"
    query = {
        "excludeForms": str(exclude_forms).lower()
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_incident_details")
    response = requests.get(url, headers=headers, params=query)
    logging.info(f"Response code for incident details: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching incident details: {response.status_code}")
        log_function_completion("fetch_incident_details", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_incident_details", start_time)
    return data

def get_meetings(job_id=None, recorder_id=None, business_unit_id=None, employee_id=None, start_date=None, end_date=None, skip=0, take=0):
    url = "https://api.hcssapps.com/safety/v1/meetings"
    query = {
        "jobId": job_id,
        "recorderId": recorder_id,
        "businessUnitId": business_unit_id,
        "employeeId": employee_id,
        "startDate": start_date,
        "endDate": end_date,
        "skip": skip,
        "take": take
    }
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_meetings")
    response = fetch_data_with_progress(url, headers, query)
    logging.info(f"Response code for meetings: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error fetching meetings: {response.status_code}")
        log_function_completion("fetch_meetings", start_time)
        return None

    data = response.json()
    log_function_completion("fetch_meetings", start_time)
    return data
