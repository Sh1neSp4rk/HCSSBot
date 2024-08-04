import logging
import os
from datetime import datetime
from .Tools.caller import fetch_all_data
from .Tools.data_saver import save_data
from .Tools.email_sender import send_email

# Create Logs directory if it doesn't exist
if not os.path.exists('Logs'):
    os.makedirs('Logs')

# Configure logging to write to a file in the Logs directory
log_filename = datetime.now().strftime("Logs/data_fetch_%Y%m%d_%H%M%S.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Starting data fetch process")

    business_units, roles, subscription_groups, jobs, users = fetch_all_data()

    attachments = []
    timestamp = datetime.now().isoformat()

    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        if roles:
            logging.info(f"Fetched roles: {roles}")
            filename = f'roles_data_{timestamp}.csv'
            save_data(roles, filename, 'csv')
            attachments.append(filename)
            logging.info(f"Saved roles data to {filename}")

        if subscription_groups:
            logging.info(f"Fetched subscription groups: {subscription_groups}")
            filename = f'subscription_groups_data_{timestamp}.csv'
            save_data(subscription_groups, filename, 'csv')
            attachments.append(filename)
            logging.info(f"Saved subscription groups data to {filename}")

        if jobs:
            logging.info(f"Fetched jobs: {jobs}")
            filename = f'jobs_data_{timestamp}.csv'
            save_data(jobs, filename, 'csv')
            attachments.append(filename)
            logging.info(f"Saved jobs data to {filename}")

        if users:
            logging.info(f"Fetched users: {users}")
            filename = f'users_data_{timestamp}.csv'
            save_data(users, filename, 'csv')
            attachments.append(filename)
            logging.info(f"Saved users data to {filename}")

        recipient_email = os.getenv('TARGET_EMAIL')
        if recipient_email:
            send_email(attachments, recipient_email)
            logging.info(f"Email sent to {recipient_email}")
        else:
            logging.error("No recipient email address found in .env")
    else:
        logging.error("No business units found")

if __name__ == "__main__":
    main()
