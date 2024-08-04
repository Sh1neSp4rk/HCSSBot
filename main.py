# main.py
import logging
import argparse
from UsersGET import get_business_units, get_jobs, get_roles, get_subscription_groups, get_all_users
from DataSaver import save_data
from EmailSender import send_email
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def fetch_and_save_data(file_type, business_unit_id):
    # Fetch and save roles
    roles = get_roles()
    if roles:
        logging.info(f"Fetched roles: {roles}")
        save_data(roles, 'roles_data', file_type)
    
    # Fetch and save subscription groups
    subscription_groups = get_subscription_groups()
    if subscription_groups:
        logging.info(f"Fetched subscription groups: {subscription_groups}")
        save_data(subscription_groups, 'subscription_groups_data', file_type)
    
    # Fetch and save jobs
    jobs = get_jobs(business_unit_id)
    if jobs:
        logging.info(f"Fetched jobs: {jobs}")
        save_data(jobs, 'jobs_data', file_type)
    
    # Fetch and save users
    users = get_all_users(business_unit_id)
    if users:
        logging.info(f"Fetched users: {users}")
        save_data(users, 'users_data', file_type)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch data from API and send it via email.')
    parser.add_argument('--file_type', type=str, choices=['csv', 'json', 'xlsx'], default='xlsx', help='The file type to save the data as.')
    parser.add_argument('--email', type=str, default='mikelamble@hotmail.com', help='The email address to send the data to.')
    parser.add_argument('--files', nargs='*', default=['roles', 'subscription_groups', 'jobs', 'users'], help='List of files to create. Options: roles, subscription_groups, jobs, users.')

    args = parser.parse_args()

    logging.info("Starting the main process")
    
    # Fetch business units
    business_units = get_business_units()
    if business_units:
        logging.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logging.info(f"Using Business Unit ID: {business_unit_id}")

        # Determine which files to create based on arguments
        if 'roles' in args.files:
            fetch_and_save_data(args.file_type, business_unit_id)
        
        if 'subscription_groups' in args.files:
            fetch_and_save_data(args.file_type, business_unit_id)
        
        if 'jobs' in args.files:
            fetch_and_save_data(args.file_type, business_unit_id)
        
        if 'users' in args.files:
            fetch_and_save_data(args.file_type, business_unit_id)
        
        # Send email with the attached file(s)
        subject = "API Data Export"
        body = "Please find attached the data export from the API."
        attachment_file = f"users_data.{args.file_type}"  # Update to send different files as needed
        send_email(subject, body, args.email, attachment_file)
    else:
        logging.error("No business units found")

if __name__ == "__main__":
    main()
