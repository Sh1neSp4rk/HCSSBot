import requests
from datetime import datetime
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, setup_function_logger, log_process_start, log_process_completion, log_error, log_function_call, log_function_completion, get_timestamp, get_last_successful_date_from_log

# Set up loggers
main_logger = setup_main_logger()
function_logger = setup_function_logger()

def log_request(url, params=None, method='GET'):
    log_process_start(main_logger, f"Request to {url}")
    main_logger.info(f"Request Method: {method}, URL: {url}, Params: {params}")

def log_response(response):
    main_logger.info(f"Response Status Code: {response.status_code}")
    try:
        main_logger.info(f"Response Data: {response.json()}")
    except ValueError:
        main_logger.info("Response Data: Non-JSON Response")

def get_last_successful_date(function_name):
    return get_last_successful_date_from_log(main_logger, function_name)

def get_HeavyJob_business_units():
    url = "https://api.hcssapps.com/heavyjob/api/v1/businessUnits"
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_jobs():
    url = "https://api.hcssapps.com/heavyjob/api/v1/jobs"
    token = get_token()
    query = {}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobcosts(job_id, start_date):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/jobs/{job_id}/costs"
    token = get_token()
    query = {"startDate": start_date}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_costcodes(business_unit_id=None, limit=1000, cursor=None):
    token = get_token()
    if not business_unit_id:
        business_units = get_HeavyJob_business_units()
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

def get_HeavyJob_jobemployees(job_id, limit=1000, cursor=None):
    token = get_token()
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

def get_HeavyJob_jobequipment(job_id, limit=1000, cursor=None):
    token = get_token()
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

def get_HeavyJob_jobmaterials(job_id, is_discontinued="false", is_deleted="false"):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/jobs/{job_id}/costTypes/jobMaterial"
    query = {"isDiscontinued": is_discontinued, "isDeleted": is_deleted}
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_materials(business_unit_id=None, is_deleted="false"):
    token = get_token()
    if not business_unit_id:
        business_units = get_HeavyJob_business_units()
        business_unit_id = business_units[0]['id'] if business_units else None

    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/costTypes/material"
    query = {"isDeleted": is_deleted}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_timecards(job_id, modified_since=None, cursor=None, limit=1000):
    token = get_token()
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

def get_HeavyJob_diaries(start_date, business_unit_id=None, cursor=None, limit=0):
    token = get_token()
    if not business_unit_id:
        business_units = get_HeavyJob_business_units()
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

def get_HeavyJob_employees(include_historical_foreman="true", business_unit_id=None):
    token = get_token()
    if not business_unit_id:
        business_units = get_HeavyJob_business_units()
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

def get_HeavyJob_equipment_types(business_unit_id=None):
    token = get_token()
    if not business_unit_id:
        business_units = get_HeavyJob_business_units()
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/equipment/types"
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_equipment(business_unit_id=None):
    token = get_token()
    if not business_unit_id:
        business_units = get_HeavyJob_business_units()
        business_unit_id = business_units[0]['id'] if business_units else None

    url = "https://api.hcssapps.com/heavyjob/api/v1/equipment"
    params = {"businessUnitId": business_unit_id}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=params, method='GET')
    response = requests.get(url, headers=headers, params=params)
    log_response(response)
    return response.json()

def get_HeavyJob_equipmenthours():
    url = "https://api.hcssapps.com/heavyjob/api/v1/equipment/hours"
    start_date = get_last_successful_date('equipment_hours')  # Fetching last successful date
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    token = get_token()
    params = {
        "startDate": start_date or '1900-01-01T00:00:00Z',  # Default to an old date if not found
        "endDate": end_date
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=params, method='GET')
    response = requests.get(url, headers=headers, params=params)
    log_response(response)
    return response.json()

def get_HeavyJob_employeehours():
    url = "https://api.hcssapps.com/heavyjob/api/v1/employee/hours"
    start_date = get_last_successful_date_from_log(main_logger, 'employee_hours')  # Fetching last successful date
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    token = get_token()
    params = {
        "startDate": start_date or '1900-01-01T00:00:00Z',  # Default to an old date if not found
        "endDate": end_date
    }
    headers = {"Authorization": f"Bearer {token}"}

    start_time = get_timestamp()
    log_function_call(function_logger, 'get_HeavyJob_employeehours', start_time)

    try:
        log_request(url, params=params, method='GET')
        response = requests.get(url, headers=headers, params=params)
        log_response(response)
        log_function_completion(function_logger, 'get_HeavyJob_employeehours', start_time)
        return response.json()
    except Exception as e:
        log_error(main_logger, f"Error in get_HeavyJob_employeehours: {e}")
        raise
