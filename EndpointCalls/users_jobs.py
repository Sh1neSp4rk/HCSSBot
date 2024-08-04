# EndpointCalls/users_jobs.py
import logging
from EndpointCalls.token_get import get_token
from Tools.progress_bars import fetch_data_with_progress

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_jobs(business_unit_id):
    endpoint = "https://api.hcssapps.com/users/api/v1/Jobs/GetJobsByBusinessUnit"
    params = {"businessUnitId": business_unit_id}
    logging.info(f"Fetching jobs for business unit ID: {business_unit_id} from {endpoint}")
    token = get_token()
    if not token:
        logging.error("Failed to retrieve token")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_data_with_progress(endpoint, headers, params).json()
