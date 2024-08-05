# Tools/caller.py
import logging
from EndpointCalls.users_business_units import get_business_units
from EndpointCalls.users_jobs import get_jobs
from EndpointCalls.users_roles import get_roles
from EndpointCalls.users_subscription_groups import get_subscription_groups
from EndpointCalls.users_users import get_all_users

status_logger = logging.getLogger('status_logger')

def fetch_all_data():
    logging.info("Fetching all data")
    
    status_logger.info("Starting fetch_all_data")
    business_units = get_business_units()
    if not business_units:
        logging.error("No business units found")
        status_logger.error("No business units found")
        return None, None, None, None, None

    roles = get_roles()
    subscription_groups = get_subscription_groups()
    jobs = get_jobs(business_units[0].get('id'))
    users = get_all_users(business_units[0].get('id'))
    
    status_logger.info("Fetched all data successfully")
    return business_units, roles, subscription_groups, jobs, users
