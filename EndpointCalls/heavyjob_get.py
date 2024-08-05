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
    logging.info(f"Response Data: {response.json()}")

def get_HeavyJob_businessunits(token):
    url = "https://api.hcssapps.com/heavyjob/api/v1/businessUnits"
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_jobs(token, business_unit_id):
    url = "https://api.hcssapps.com/heavyjob/api/v1/jobs"
    query = {"businessUnitId": business_unit_id}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobcosts(token, job_id, effective_date, start_date):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/jobs/{job_id}/costs"
    query = {"effectiveDate": effective_date, "startDate": start_date}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_costcodes(token, accounting_template_name, job_id, business_unit_id, cost_code_id, limit=1000, cursor=None):
    url = "https://api.hcssapps.com/heavyjob/api/v1/costCodes"
    query = {
        "accountingTemplateName": accounting_template_name,
        "jobId": job_id,
        "businessUnitId": business_unit_id,
        "costCodeId": cost_code_id,
        "limit": limit,
        "cursor": cursor
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobemployees(token, business_unit_id, job_id, employee_id=None, limit=1000, cursor=None):
    url = "https://api.hcssapps.com/heavyjob/api/v1/jobEmployees"
    query = {
        "businessUnitId": business_unit_id,
        "jobId": job_id,
        "employeeId": employee_id,
        "limit": limit,
        "cursor": cursor
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_jobequipment(token, business_unit_id, job_id, equipment_id=None, limit=1000, cursor=None):
    url = "https://api.hcssapps.com/heavyjob/api/v1/jobEquipment"
    query = {
        "businessUnitId": business_unit_id,
        "jobId": job_id,
        "equipmentId": equipment_id,
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

def get_HeavyJob_materials(token, business_unit_id, is_deleted="false"):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/costTypes/material"
    query = {"isDeleted": is_deleted}
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_timecards(token, job_id, foreman_id=None, employee_id=None, start_date=None, end_date=None, modified_since=None, only_tm="false", cursor=None, limit=1000):
    url = "https://api.hcssapps.com/heavyjob/api/v1/timeCardInfo"
    query = {
        "jobId": job_id,
        "foremanId": foreman_id,
        "employeeId": employee_id,
        "startDate": start_date,
        "endDate": end_date,
        "modifiedSince": modified_since,
        "onlyTM": only_tm,
        "cursor": cursor,
        "limit": limit
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params={k: v for k, v in query.items() if v is not None}, method='GET')
    response = requests.get(url, headers=headers, params={k: v for k, v in query.items() if v is not None})
    log_response(response)
    return response.json()

def get_HeavyJob_user(token, user_id):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_diaries(token, business_unit_id, job_ids, job_tag_ids, foreman_ids, job_status, start_date, end_date, cursor=None, limit=0):
    url = "https://api.hcssapps.com/heavyjob/api/v1/diaries/search"
    payload = {
        "businessUnitId": business_unit_id,
        "jobIds": job_ids,
        "jobTagIds": job_tag_ids,
        "foremanIds": foreman_ids,
        "jobStatus": job_status,
        "startDate": start_date,
        "endDate": end_date,
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

def get_HeavyJob_employees(token, business_unit_id, accounting_template_name="string", is_active="true", is_deleted="false", is_foreman="true", include_historical_foreman="true"):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/employees"
    query = {
        "accountingTemplateName": accounting_template_name,
        "isActive": is_active,
        "isDeleted": is_deleted,
        "isForeman": is_foreman,
        "includeHistoricalForeman": include_historical_foreman
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_equipment_types(token, business_unit_id):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/equipment/types"
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, method='GET')
    response = requests.get(url, headers=headers)
    log_response(response)
    return response.json()

def get_HeavyJob_equipment(token, business_unit_id, accounting_template_name="string"):
    url = f"https://api.hcssapps.com/heavyjob/api/v1/businessUnits/{business_unit_id}/equipment"
    query = {
        "accountingTemplateName": accounting_template_name,
        "isActive": "true",
        "isDeleted": "false"
    }
    headers = {"Authorization": f"Bearer {token}"}
    log_request(url, params=query, method='GET')
    response = requests.get(url, headers=headers, params=query)
    log_response(response)
    return response.json()

def get_HeavyJob_equipmenthours(token, business_unit_id, equipment_ids, modified_since, linked_employee_ids, job_ids, job_tag_ids, foreman_ids, start_date, end_date, cursor=None, limit=500):
    url = "https://api.hcssapps.com/heavyjob/api/v1/hours/equipment"
    payload = {
        "businessUnitId": business_unit_id,
        "includeAllJobs": True,
        "equipmentIds": equipment_ids,
        "modifiedSince": modified_since,
        "linkedEmployeeIds": linked_employee_ids,
        "jobIds": job_ids,
        "jobTagIds": job_tag_ids,
        "foremanIds": foreman_ids,
        "startDate": start_date,
        "endDate": end_date,
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

def get_HeavyJob_employeehours(token, business_unit_id, modified_since, employee_ids, job_ids, job_tag_ids, foreman_ids, start_date, end_date, cursor=None, limit=500):
    url = "https://api.hcssapps.com/heavyjob/api/v1/hours/employees"
    payload = {
        "businessUnitId": business_unit_id,
        "includeAllJobs": True,
        "modifiedSince": modified_since,
        "employeeIds": employee_ids,
        "jobIds": job_ids,
        "jobTagIds": job_tag_ids,
        "foremanIds": foreman_ids,
        "startDate": start_date,
        "endDate": end_date,
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
