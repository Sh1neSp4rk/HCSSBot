# EndpointCalls/heavybidestimates_get.py
import logging
import requests
from datetime import datetime
import os

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

def fetch_business_units(token):
    url = "https://api.hcssapps.com/heavybid/api/v2/integration/businessunits"
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_business_units")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        logging.error(f"Error fetching business units: {e}")
        log_function_completion("fetch_business_units", start_time)
        return None
    
    logging.info(f"Response code for business units: {response.status_code}")
    data = response.json()
    log_function_completion("fetch_business_units", start_time)
    return data

def fetch_database_partitions(token, business_unit_id):
    url = f"https://api.hcssapps.com/heavybid/api/v2/integration/businessunits/{business_unit_id}/partitions"
    headers = {"Authorization": f"Bearer {token}"}
    start_time = log_function_call("fetch_database_partitions")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        logging.error(f"Error fetching database partitions for {business_unit_id}: {e}")
        log_function_completion("fetch_database_partitions", start_time)
        return None
    
    logging.info(f"Response code for database partitions: {response.status_code}")
    data = response.json()
    log_function_completion("fetch_database_partitions", start_time)
    return data

def main():
    token = os.getenv("HEAVYBID_API_TOKEN")  # Fetch token from environment variables
    if not token:
        logging.error("API token is not set")
        return
    
    # Fetch business units
    business_units = fetch_business_units(token)
    if not business_units:
        logging.error("No business units data retrieved")
        return
    
    # Fetch partitions for each business unit
    all_partitions = []
    for business_unit in business_units.get("results", []):
        business_unit_id = business_unit.get("id")
        if not business_unit_id:
            continue
        
        partitions = fetch_database_partitions(token, business_unit_id)
        if partitions:
            all_partitions.extend(partitions.get("results", []))
    
    # Print or process all partitions as needed
    print(all_partitions)

if __name__ == "__main__":
    main()
