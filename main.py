# main.py
import logging
from Tools.caller import fetch_all_data
from Tools.data_saver import save_data
from Tools.email_sender import send_email

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting data fetch process")

    business_units, roles, subscription_groups, jobs, users = fetch_all_data()

    attachments = []

    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        if roles:
            logging.info(f"Fetched roles: {roles}")
            save_data(roles, 'roles_data.csv', 'csv')
            attachments.append('roles_data.csv')

        if subscription_groups:
            logging.info(f"Fetched subscription groups: {subscription_groups}")
            save_data(subscription_groups, 'subscription_groups_data.csv', 'csv')
            attachments.append('subscription_groups_data.csv')

        if jobs:
            logging.info(f"Fetched jobs: {jobs}")
            save_data(jobs, 'jobs_data.csv', 'csv')
            attachments.append('jobs_data.csv')

        if users:
            logging.info(f"Fetched users: {users}")
            save_data(users, 'users_data.csv', 'csv')
            attachments.append('users_data.csv')

        recipient_email = os.getenv('TARGET_EMAIL')
        if recipient_email:
            send_email(attachments, recipient_email)
        else:
            logging.error("No recipient email address found in .env")

    else:
        logging.error("No business units found")

if __name__ == "__main__":
    main()
