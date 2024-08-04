# EndpointCalls/caller.py
from EndpointCalls.users_business_units import get_business_units
from EndpointCalls.users_jobs import get_jobs
from EndpointCalls.users_roles import get_roles
from EndpointCalls.users_subscription_groups import get_subscription_groups
from EndpointCalls.users_users import get_all_users

def fetch_all_data():
    business_units = get_business_units()
    if not business_units:
        return None, None, None, None, None
    
    business_unit_id = business_units[0].get('id')

    roles = get_roles()
    subscription_groups = get_subscription_groups()
    jobs = get_jobs(business_unit_id)
    users = get_all_users(business_unit_id)

    return business_units, roles, subscription_groups, jobs, users
