import argparse
import os
from EndpointCalls.UsersGET import fetch_all_users_data
from EndpointCalls.TokenGET import get_access_token
from Tools.data_saver import save_data
from Tools.email_sender import send_email
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default values
DEFAULT_FILE_TYPE = 'xlsx'
DEFAULT_EMAIL = os.getenv('TARGET_EMAIL')

def main(file_type, email, files_to_create):
    # Fetch the access token
    token = get_access_token()
    
    # Fetch data and save to files
    attachments = []
    if 'roles' in files_to_create:
        roles_data = fetch_all_users_data(token)
        roles_file = save_data(roles_data, 'roles', file_type)
        attachments.append(roles_file)

    if 'subscription_groups' in files_to_create:
        subscription_groups_data = fetch_all_users_data(token)
        subscription_groups_file = save_data(subscription_groups_data, 'subscription_groups', file_type)
        attachments.append(subscription_groups_file)

    # Add more if conditions for other file types...

    # Send email with the generated files
    send_email(attachments, email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch API data, save it, and email it")
    parser.add_argument("--file_type", type=str, default=DEFAULT_FILE_TYPE, help="The file type to save data as (csv, json, xlsx)")
    parser.add_argument("--email", type=str, default=DEFAULT_EMAIL, help="The email address to send the data to")
    parser.add_argument("--files", nargs='*', default=['roles', 'subscription_groups'], help="The list of files to create")

    args = parser.parse_args()
    main(args.file_type, args.email, args.files)
