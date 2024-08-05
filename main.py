import argparse
import logging
import os
from datetime import datetime
from Tools.caller import fetch_all_data
from Tools.data_saver import save_data
from Tools.email_sender import send_email
from Tools.cleanup_files import cleanup_files

# Clean up the Files folder
cleanup_files('Files')

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and process data.")
    parser.add_argument('--file_type', default='xlsx', choices=['csv', 'json', 'xlsx'], help="The file type to save the data as.")
    parser.add_argument('--email', default='mikelamble@hotmail.com', help="The email address to send the data to.")
    parser.add_argument('--files', nargs='*', help="The specific files to create (e.g., roles, subscription_groups, jobs, users).")
    return parser.parse_args()

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
    args = parse_args()
    logging.info(f"Starting data fetch process with file type: {args.file_type}, email: {args.email}, files: {args.files}")

    business_units, roles, subscription_groups, jobs, users = fetch_all_data()

    attachments = []

    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        if args.files is None or 'roles' in args.files:
            if roles:
                logging.info(f"Fetched roles: {roles}")
                filename = save_data(roles, 'roles', args.file_type)
                attachments.append(filename)
                logging.info(f"Saved roles data to {filename}")

        if args.files is None or 'subscription_groups' in args.files:
            if subscription_groups:
                logging.info(f"Fetched subscription groups: {subscription_groups}")
                filename = save_data(subscription_groups, 'subscription_groups', args.file_type)
                attachments.append(filename)
                logging.info(f"Saved subscription groups data to {filename}")

        if args.files is None or 'jobs' in args.files:
            if jobs:
                logging.info(f"Fetched jobs: {jobs}")
                filename = save_data(jobs, 'jobs', args.file_type)
                attachments.append(filename)
                logging.info(f"Saved jobs data to {filename}")

        if args.files is None or 'users' in args.files:
            if users:
                logging.info(f"Fetched users: {users}")
                filename = save_data(users, 'users', args.file_type)
                attachments.append(filename)
                logging.info(f"Saved users data to {filename}")

        send_email(attachments, args.email)
        logging.info(f"Email sent to {args.email}")
    else:
        logging.error("No business units found")

if __name__ == "__main__":
    main()
