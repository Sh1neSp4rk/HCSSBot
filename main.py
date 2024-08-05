import logging
import os
import sys
from datetime import datetime
from Tools.caller import fetch_all_data
from Tools.data_saver import save_data
from Tools.email_sender import send_email
import argparse

# Ensure the current directory is in the PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create Logs directory if it doesn't exist
if not os.path.exists('Logs'):
    os.makedirs('Logs')

# Configure logging to write to a file in the Logs directory
log_filename = datetime.now().strftime("Logs/data_fetch_%Y%m%d_%H%M%S.log")
status_log_filename = "Logs/status_codes.log"

logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

status_logger = logging.getLogger('status_logger')
status_handler = logging.FileHandler(status_log_filename, mode='w')  # overwrite each run
status_handler.setLevel(logging.DEBUG)
status_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
status_handler.setFormatter(status_formatter)
status_logger.addHandler(status_handler)

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and save data from HCSS API")
    parser.add_argument('--file-type', type=str, default='xlsx', choices=['csv', 'json', 'xlsx'],
                        help="File type to save data as (default: xlsx)")
    parser.add_argument('--email', type=str, default='mikelamble@hotmail.com',
                        help="Email address to send the data to (default: mikelamble@hotmail.com)")
    parser.add_argument('--files', type=str, nargs='+', choices=['roles', 'subscription_groups', 'jobs', 'users'],
                        help="List of files to create (default: all)")

    return parser.parse_args()

def main():
    args = parse_args()
    logging.info(f"Starting data fetch process with file type: {args.file_type}, email: {args.email}, files: {args.files}")

    business_units, roles, subscription_groups, jobs, users = fetch_all_data()

    attachments = []
    timestamp = datetime.now().isoformat()

    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        if args.files is None or 'roles' in args.files:
            if roles:
                logging.info(f"Fetched roles: {roles}")
                filename = f'roles_data_{timestamp}.{args.file_type}'
                save_data(roles, filename, args.file_type)
                attachments.append(filename)
                logging.info(f"Saved roles data to {filename}")

        if args.files is None or 'subscription_groups' in args.files:
            if subscription_groups:
                logging.info(f"Fetched subscription groups: {subscription_groups}")
                filename = f'subscription_groups_data_{timestamp}.{args.file_type}'
                save_data(subscription_groups, filename, args.file_type)
                attachments.append(filename)
                logging.info(f"Saved subscription groups data to {filename}")

        if args.files is None or 'jobs' in args.files:
            if jobs:
                logging.info(f"Fetched jobs: {jobs}")
                filename = f'jobs_data_{timestamp}.{args.file_type}'
                save_data(jobs, filename, args.file_type)
                attachments.append(filename)
                logging.info(f"Saved jobs data to {filename}")

        if args.files is None or 'users' in args.files:
            if users:
                logging.info(f"Fetched users: {users}")
                filename = f'users_data_{timestamp}.{args.file_type}'
                save_data(users, filename, args.file_type)
                attachments.append(filename)
                logging.info(f"Saved users data to {filename}")

        send_email(attachments, args.email)
        logging.info(f"Email sent to {args.email}")
    else:
        logging.error("No business units found")

if __name__ == "__main__":
    main()
