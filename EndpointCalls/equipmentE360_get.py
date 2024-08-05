# EndpointCalls/equipmentE360_get.py
import requests
import logging
from datetime import datetime
from Tools.progress_bars import Bar
from Tools.data_saver import save_data
from Tools.caller import get_last_successful_date, set_last_successful_date
from EndpointCalls.token_get import get_token

# Setting up logging
logging.basicConfig(filename='Logs/equipment360_get.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logger():
    logger = logging.getLogger('equipment360')
    return logger

logger = setup_logger()

def get_headers():
    token = get_token()  # Assuming this function fetches the current token
    headers = {"Authorization": f"Bearer {token}"}
    return headers

def fetch_data(url, params=None):
    headers = get_headers()
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def log_function_call(function_name, status):
    logger.info(f"{function_name} - {status}")

def fetch_business_units(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/businessUnits"
    logger.info("Fetching Business Units")
    data = fetch_data(url)
    save_data(data, 'business_units', file_type)
    log_function_call("fetch_business_units", "Completed")
    set_last_successful_date('business_units')
    return data

def fetch_fuel_costs(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/costs/fuel"
    start_date = get_last_successful_date('fuel_costs')  # Fetching last successful date
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "startDate": start_date,
        "endDate": end_date,
    }
    logger.info("Fetching Fuel Costs")
    data = fetch_data(url, params=params)
    save_data(data, 'fuel_costs', file_type)
    log_function_call("fetch_fuel_costs", "Completed")
    set_last_successful_date('fuel_costs')
    return data

def fetch_work_order_costs(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/costs/workOrders"
    params = {
        "businessUnitId": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    }
    logger.info("Fetching Work Order Costs")
    data = fetch_data(url, params=params)
    save_data(data, 'work_order_costs', file_type)
    log_function_call("fetch_work_order_costs", "Completed")
    set_last_successful_date('work_order_costs')
    return data

def fetch_work_order_details(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/costs/workOrdersExtended"
    params = {
        "businessUnitId": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
        "count": "0",
        "cursor": "0"
    }
    logger.info("Fetching Work Order Details")
    data = fetch_data(url, params=params)
    save_data(data, 'work_order_details', file_type)
    log_function_call("fetch_work_order_details", "Completed")
    set_last_successful_date('work_order_details')
    return data

def fetch_custom_fields(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/customField"
    logger.info("Fetching Custom Fields")
    data = fetch_data(url)
    save_data(data, 'custom_fields', file_type)
    log_function_call("fetch_custom_fields", "Completed")
    set_last_successful_date('custom_fields')
    return data

def fetch_custom_field_categories(file_type):
    url = "https://api.hcssapps.com/e360/api/v1/customFieldCategories"
    params = {
        "categoryType": "equipment"
    }
    logger.info("Fetching Custom Field Categories")
    data = fetch_data(url, params=params)
    save_data(data, 'custom_field_categories', file_type)
    log_function_call("fetch_custom_field_categories", "Completed")
    set_last_successful_date('custom_field_categories')
    return data

def main(file_type='json'):
    functions = [
        fetch_business_units,
        fetch_fuel_costs,
        fetch_work_order_costs,
        fetch_work_order_details,
        fetch_custom_fields,
        fetch_custom_field_categories
    ]

    with Bar('Processing', max=len(functions)) as bar:
        for func in functions:
            try:
                func(file_type)
                bar.next()
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                bar.next()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch data from equipmentE360 API.")
    parser.add_argument('--file_type', type=str, default='json', choices=['json', 'csv', 'xlsx'],
                        help='Specify the file type to save the data (json, csv, xlsx).')
    args = parser.parse_args()
    main(args.file_type)
