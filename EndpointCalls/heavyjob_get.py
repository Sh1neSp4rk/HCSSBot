# EndpointCalls/heavyjob_get.py
import requests
import logging
from datetime import datetime
from EndpointCalls.token_get import get_token

# Configure logging
logging.basicConfig(
    filename='Logs/heavyjob_get.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_request(url, params=None, method='GET'):
    logging.info(f"Request Method: {method}, URL: {url}, Params: {params}")

def log_response(response):
    logging.info(f"Response Status Code: {response.status_code}")
    try:
        logging.info(f"Response Data: {response.json()}")
    except ValueError:
        logging.info("Response Data: Non-JSON Response")

def get_HeavyJob_business_units(token):
    url = "https://api.hcssapps.com/heavyjob/api/v1/businessUnits"
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_jobs(token):
    url = "https://api.hcssapps.com/heavyjob/api/v1/jobs"
    query = {}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobcosts(token, job_id, start_date):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/jobs/{job_id}/costs"
    query = {"startDate": start_date}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_costcodes(token, business_unit_id=None, limit=1000, cursor=None):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/costCodes"
    query = {
        "limit": limit,
        "cursor": cursor
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobemployees(token, job_id, limit=1000, cursor=None):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/jobEmployees"
    query = {
        "jobId": job_id,
        "limit": limit,
        "cursor": cursor
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobequipment(token, job_id, limit=1000, cursor=None):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/jobEquipment"
    query = {
        "jobId": job_id,
        "limit": limit,
        "cursor": cursor
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobmaterials(token, job_id, is_discontinued="false", is_deleted="false"):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/jobs/{job_id}/costTypes/jobMaterial"
    query = {"isDiscontinued": is_discontinued, "isDeleted": is_deleted}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_materials(token, business_unit_id=None, is_deleted="false"):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/costTypes/material"
    query = {"isDeleted": is_deleted}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_timecards(token, job_id, modified_since=None, cursor=None, limit=1000):
    url = "https://api.hcssapps.com/heavyjob/api/v1/timeCardInfo"
    query = {
        "jobId": job_id,
        "modifiedSince": modified_since,
        "cursor": cursor,
        "limit": limit
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params={k: v for k, v in query.items() if v is not None}, method='GET')
    response = requests.get(url, headers=headers, params={k: v for k, v in query.items() if v is not None})
    log_response(response)
    return response.json()

def get_HeavyJob_diaries(token, start_date, business_unit_id=None, cursor=None, limit=0):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/diaries/search"
    payload = {
        "businessUnitId": business_unit_id,
        "startDate": start_date,
        "cursor": cursor,
        "limit": limit
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    log_request(url, params=payload, method='POST')
    response = requests.post(url, json=payload, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_employees(token, include_historical_foreman="true", business_unit_id=None):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/employees"
    query = {
        "includeHistoricalForeman": include_historical_foreman
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_equipment_types(token, business_unit_id=None):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/equipment/types"
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_equipment(token, business_unit_id=None):
    if not business_unit_id:
        business_units = get_HeavyJob_business_units(token)
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/equipment"
    params = {"businessUnitId": business_unit_id}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=params, method='GET')
    response = requests.get(url, headers=headers, params=params)
    log_response(response)
    return response.json()

def get_HeavyJob_equipmenthours(token):
    url = "https://api.hcssapps.com/heavyjob/api/v1/equipment/hours"
    start_date = get_last_successful_date_from_log(logger, 'equipment_hours')  # Fetching last successful date
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "startDate": start_date or '1900-01-01T00:00:00Z',  # Default to an old date if not found
        "endDate": end_date
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=params, method='GET')
    response = requests.get(url, headers=headers, params=params)
    log_response(response)
    return response.json()

def get_HeavyJob_employeehours(token):
    url = "https://api.hcssapps.com/heavyjob/api/v1/employee/hours"
    start_date = get_last_successful_date_from_log(logger, 'employee_hours')  # Fetching last successful date
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "startDate": start_date or '1900-01-01T00:00:00Z',  # Default to an old date if not found
        "endDate": end_date
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=params, method='GET')
    response = requests.get(url, headers=headers, params=params)
    log_response(response)
    return response.json()
