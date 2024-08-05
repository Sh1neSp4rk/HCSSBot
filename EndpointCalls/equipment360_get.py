import requests
from datetime import datetime
from Tools.progress_bars import fetch_data_with_progress
from Tools.data_saver import save_data
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, set_last_successful_date, get_last_successful_date_from_log

# Setting up logging
logger = setup_main_logger()

def get_headers():
    token = get_token()
    return {"Authorization": f"Bearer {token}"}

def fetch_data(url, params=None):
    headers = get_headers()
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def log_function_call(function_name, status):
    logger.info(f"{function_name} - {status}")

def get_EquipmentE360_business_units(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/businessUnits"
    logger.info("Fetching Business Units")
    data = fetch_data(url)
    save_data(data, 'business_units', file_type)
    log_function_call("fetch_business_units", "Completed")
    set_last_successful_date(logger, 'business_units')
    return [unit['id'] for unit in data['results']]

def get_EquipmentE360_fuel_costs(file_type, business_unit_ids=None):
    if not business_unit_ids:
        business_unit_ids = get_EquipmentE360_business_units(file_type)

    url = "https://api.hcssapps.com/e360/api/v1/costs/fuel"
    start_date = get_last_successful_date_from_log(logger, 'fuel_costs')
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "startDate": start_date or '1900-01-01T00:00:00Z',
        "endDate": end_date,
    }
    logger.info("Fetching Fuel Costs")
    data = fetch_data(url, params=params)
    save_data(data, 'fuel_costs', file_type)
    log_function_call("fetch_fuel_costs", "Completed")
    set_last_successful_date(logger, 'fuel_costs')
    return data

def get_EquipmentE360_work_order_costs(file_type, business_unit_ids=None):
    if not business_unit_ids:
        business_unit_ids = get_EquipmentE360_business_units(file_type)

    url = "https://api.hcssapps.com/e360/api/v1/costs/workOrders"
    all_data = []
    for unit_id in business_unit_ids:
        params = {"businessUnitId": unit_id}
        logger.info(f"Fetching Work Order Costs for Business Unit ID: {unit_id}")
        data = fetch_data(url, params=params)
        all_data.extend(data.get('results', []))
        fetch_data_with_progress.update_progress(unit_id, len(business_unit_ids))
    save_data(all_data, 'work_order_costs', file_type)
    log_function_call("fetch_work_order_costs", "Completed")
    set_last_successful_date(logger, 'work_order_costs')
    return all_data

def get_EquipmentE360_work_order_details(file_type, business_unit_ids=None):
    if not business_unit_ids:
        business_unit_ids = get_EquipmentE360_business_units(file_type)

    url = "https://api.hcssapps.com/e360/api/v1/costs/workOrdersExtended"
    all_data = []
    for unit_id in business_unit_ids:
        params = {
            "businessUnitId": unit_id,
            "count": "0",
            "cursor": "0"
        }
        logger.info(f"Fetching Work Order Details for Business Unit ID: {unit_id}")
        data = fetch_data(url, params=params)
        all_data.extend(data.get('results', []))
        fetch_data_with_progress.update_progress(unit_id, len(business_unit_ids))
    save_data(all_data, 'work_order_details', file_type)
    log_function_call("fetch_work_order_details", "Completed")
    set_last_successful_date(logger, 'work_order_details')
    return all_data

def get_EquipmentE360_custom_fields(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/customField"
    logger.info("Fetching Custom Fields")
    data = fetch_data(url)
    save_data(data, 'custom_fields', file_type)
    log_function_call("fetch_custom_fields", "Completed")
    set_last_successful_date(logger, 'custom_fields')
    return data

def get_EquipmentE360_custom_field_categories(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/customFieldCategories"
    logger.info("Fetching Custom Field Categories")
    data = fetch_data(url)
    save_data(data, 'custom_field_categories', file_type)
    log_function_call("fetch_custom_field_categories", "Completed")
    set_last_successful_date(logger, 'custom_field_categories')
    return data
