import logging
from UsersGET import get_business_units, get_jobs, get_roles, get_subscription_groups, get_all_users
from data_saver import save_data

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting data fetch process")

    # Fetch business units
    business_units = get_business_units()
    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        # Fetch and save roles
        roles = get_roles()
        if roles:
            logging.info(f"Fetched roles: {roles}")
            save_data(roles, 'roles_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed

        # Fetch and save subscription groups
        subscription_groups = get_subscription_groups()
        if subscription_groups:
            logging.info(f"Fetched subscription groups: {subscription_groups}")
            save_data(subscription_groups, 'subscription_groups_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed

        # Fetch and save jobs
        jobs = get_jobs(business_unit_id)
        if jobs:
            logging.info(f"Fetched jobs: {jobs}")
            save_data(jobs, 'jobs_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed

        # Fetch and save users
        users = get_all_users(business_unit_id)
        if users:
            logging.info(f"Fetched users: {users}")
            save_data(users, 'users_data.csv', 'csv')  # Change 'csv' to 'excel' or 'json' as needed
    else:
        logging.error("No business units found")

if __name__ == "__main__":
    main()
