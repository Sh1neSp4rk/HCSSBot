# EndpointCalls/heavyjob_get.py
import requests

# Constants
BASE_URL = "https://api.hcssapps.com/heavyjob/api/v1"
AUTH_HEADER = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkREOEVCNjJFQUUzNTQ3MDNFMDI0QTZFMTZGMzQxMzdDNTA0QURFMEVSUzI1NiIsIng1dCI6IjNZNjJMcTQxUndQZ0pLYmhielFUZkZCSzNnNCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2lkZW50aXR5Lmhjc3NhcHBzLmNvbSIsIm5iZiI6MTcyMjgzMDMxNiwiaWF0IjoxNzIyODMwMzE2LCJleHAiOjE3MjI4MzM5MTYsImF1ZCI6WyJpbmNpZGVudHM6cmVhZCIsIm1lZXRpbmdzOnJlYWQiLCJodHRwczovL2lkZW50aXR5Lmhjc3NhcHBzLmNvbS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiaW5jaWRlbnRzOnJlYWQiLCJtZWV0aW5nczpyZWFkIl0sImNsaWVudF9pZCI6IndidXFrdHNyZGowMDdsN21remZqM3c2OHFtYjVyZzZrIiwiaHR0cDovL2NyZWRlbnRpYWxzLmhjc3NhcHBzLmNvbS9zY2hlbWFzLzIwMTUvMDkvaWRlbnRpdHkvY2xhaW1zL2NvbXBhbnlpZCI6ImRlZDA3MmVmLWUyYzgtNGFmMi04NjY3LTdkOTIxNmRkM2ViZCIsInJlcXVlc3RTb3VyY2UiOiJDdXN0b21lciJ9.OI9LrXv2tyt16fYrZOegFyTjJo0-S2epaC_CJu6l2q2X-JgW4EEsAbVN3_lN_QlRBRN0-2PRrIq9LKP0F5mr_ODcNS7c-x1J8D0BdwDL3RauFyh9uZw_AIggXDQWg3ZiAPoUNkn-mIKL0zmHskLS95PRIYmHwdK2Mqh6dw2FHBzplNBtkeptiEx4u1h6PRlcC0hkFn6G41oxtYWhhspYgIuA02MluxqNn8IsBJHHJ-pxmLX0oL9iFKnBC36z0gm9UI3aSQpLpAOEd-j_Dw9APyomJbbs7j-7ZR5Wyszv0nTR7BvNN19WZZAUH-shBD9EZTNDQNsDc2As44FIJqvL-g"
}

def get_business_units():
    url = f"{BASE_URL}/businessUnits"
    response = requests.get(url, headers=AUTH_HEADER)
    return response.json()

def get_job_costs(job_id, effective_date, start_date):
    url = f"{BASE_URL}/jobs/{job_id}/costs"
    query = {
        "effectiveDate": effective_date,
        "startDate": start_date
    }
    response = requests.get(url, headers=AUTH_HEADER, params=query)
    return response.json()

def get_cost_adjustments(business_unit_id):
    url = f"{BASE_URL}/businessUnits/{business_unit_id}/costAdjustments"
    response = requests.get(url, headers=AUTH_HEADER)
    return response.json()

def get_cost_codes(accounting_template_name, job_id, business_unit_id, cost_code_id, limit, cursor):
    url = f"{BASE_URL}/costCodes"
    query = {
        "accountingTemplateName": accounting_template_name,
        "jobId": job_id,
        "businessUnitId": business_unit_id,
        "costCodeId": cost_code_id,
        "limit": limit,
        "cursor": cursor
    }
    response = requests.get(url, headers=AUTH_HEADER, params=query)
    return response.json()

def get_employees(business_unit_id, accounting_template_name, is_active, is_deleted, is_foreman, include_historical_foreman):
    url = f"{BASE_URL}/businessUnits/{business_unit_id}/employees"
    query = {
        "accountingTemplateName": accounting_template_name,
        "isActive": is_active,
        "isDeleted": is_deleted,
        "isForeman": is_foreman,
        "includeHistoricalForeman": include_historical_foreman
    }
    response = requests.get(url, headers=AUTH_HEADER, params=query)
    return response.json()

def get_equipment(business_unit_id, accounting_template_name, is_active, is_deleted):
    url = f"{BASE_URL}/businessUnits/{business_unit_id}/equipment"
    query = {
        "accountingTemplateName": accounting_template_name,
        "isActive": is_active,
        "isDeleted": is_deleted
    }
    response = requests.get(url, headers=AUTH_HEADER, params=query)
    return response.json()

if __name__ == "__main__":
    # Example usage
    print("Business Units:", get_business_units())
    # Replace with actual values for other calls
    # print("Job Costs:", get_job_costs("YOUR_jobId", "2019-08-24T14:15:22Z", "2019-08-24T14:15:22Z"))
    # print("Cost Adjustments:", get_cost_adjustments("YOUR_businessUnitId"))
    # print("Cost Codes:", get_cost_codes("string", "497f6eca-6276-4993-bfeb-53cbbbba6f08", "497f6eca-6276-4993-bfeb-53cbbbba6f08", "497f6eca-6276-4993-bfeb-53cbbbba6f08", "1000", "string"))
    # print("Employees:", get_employees("YOUR_businessUnitId", "string", "true", "false", "true", "true"))
    # print("Equipment:", get_equipment("YOUR_businessUnitId", "string", "true", "false"))
