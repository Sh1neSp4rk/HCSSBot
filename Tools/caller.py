# Tools/caller.py
import logging
from EndpointCalls.users_get import get_business_units, get_jobs, get_roles, get_subscription_groups, get_all_users

# Configure logging to a file
logging.basicConfig(
    filename='Logs/data_fetch.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

status_logger = logging.getLogger('status_logger')

def fetch_all_data():
    logging.info("Starting fetch_all_data")
    status_logger.info("Starting fetch_all_data")

    # Fetch business units
    get_business_units()

    # Fetch roles
    get_roles()

    # Fetch subscription groups
    get_subscription_groups()

    # Fetch jobs and users
    business_unit_id = get_business_unit_id()  # Define this function to get the business unit ID if needed
    if not business_unit_id:
        logging.error("Business unit ID is missing")
        status_logger.error("Business unit ID is missing")
        return

    get_jobs(business_unit_id)
    get_all_users(business_unit_id)

    status_logger.info("Fetched all data successfully")

def get_business_unit_id():
    # Dummy implementation to return a sample business unit ID
    # Replace this with the actual method to retrieve business unit ID
    return 'sample-business-unit-id'
