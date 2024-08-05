import argparse
from datetime import datetime
from Tools.logger import setup_logger, log_process_start, log_process_completion, log_error
from Tools.data_saver import save_data
from Tools.email_sender import send_email
from Tools.cleanup_files import cleanup_files

# Clean up the Files folder
cleanup_files('Files')

# Set up logger
log_filename = datetime.now().strftime("data_fetch_%Y%m%d_%H%M%S.log")
logger = setup_logger(log_filename=log_filename)

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and process data.")
    parser.add_argument('--file_type', default='xlsx', choices=['csv', 'json', 'xlsx'], help="The file type to save the data as.")
    parser.add_argument('--email', default='mikelamble@hotmail.com', help="The email address to send the data to.")
    parser.add_argument('--files', nargs='*', help="The specific files to create (e.g., roles, subscription_groups, jobs, users).")
    return parser.parse_args()

def fetch_all_data():
    log_process_start(logger, "fetch_all_data")

    # Fetch data
    business_units = get_business_units()
    roles = get_roles()
    subscription_groups = get_subscription_groups()

    business_unit_id = get_business_unit_id()  # Define this function to get the business unit ID if needed
    if not business_unit_id:
        log_error(logger, "Business unit ID is missing")
        return None, None, None, None, None

    jobs = get_jobs(business_unit_id)
    users = get_users(business_unit_id)

    log_process_completion(logger, "fetch_all_data")
    return business_units, roles, subscription_groups, jobs, users

def main():
    args = parse_args()
    logger.info(f"Starting data fetch process with file type: {args.file_type}, email: {args.email}, files: {args.files}")

    business_units, roles, subscription_groups, jobs, users = fetch_all_data()

    attachments = []

    if business_units:
        logger.info(f"Fetched business units: {business_units}")
        business_unit_id = business_units[0].get('id')
        logger.info(f"Using Business Unit ID: {business_unit_id}")

        if args.files is None or 'roles' in args.files:
            if roles:
                logger.info(f"Fetched roles: {roles}")
                filename = save_data(roles, 'roles', args.file_type)
                attachments.append(filename)
                logger.info(f"Saved roles data to {filename}")

        if args.files is None or 'subscription_groups' in args.files:
            if subscription_groups:
                logger.info(f"Fetched subscription groups: {subscription_groups}")
                filename = save_data(subscription_groups, 'subscription_groups', args.file_type)
                attachments.append(filename)
                logger.info(f"Saved subscription groups data to {filename}")

        if args.files is None or 'jobs' in args.files:
            if jobs:
                logger.info(f"Fetched jobs: {jobs}")
                filename = save_data(jobs, 'jobs', args.file_type)
                attachments.append(filename)
                logger.info(f"Saved jobs data to {filename}")

        if args.files is None or 'users' in args.files:
            if users:
                logger.info(f"Fetched users: {users}")
                filename = save_data(users, 'users', args.file_type)
                attachments.append(filename)
                logger.info(f"Saved users data to {filename}")

        send_email(attachments, args.email)
        logger.info(f"Email sent to {args.email}")
    else:
        logger.error("No business units found")

if __name__ == "__main__":
    main()
