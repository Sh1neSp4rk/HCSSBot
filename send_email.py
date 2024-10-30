# send_email.py

import os
import datetime
import yagmail
from dotenv import load_dotenv
from utils_logging import logger  # Import the logger instance directly

load_dotenv()  # Load environment variables from .env file

EMAIL = os.getenv("EMAIL")  # Your sending email
PASSWORD = os.getenv("PASSWORD")  # Your sending email password
TARGET_EMAIL = os.getenv("TARGET_EMAIL")  # Email to send to

def send_email():

    downloads_folder = "downloads"
    
    # Check if the downloads folder exists
    if not os.path.exists(downloads_folder):
        logger.error(f"Downloads folder does not exist: {downloads_folder}")
        return  # Exit if the downloads folder does not exist

    files = os.listdir(downloads_folder)

    # Check if the downloads folder is empty
    if not files:
        logger.error("No files in the downloads folder. Exiting without sending email.")
        return  # Exit if there are no files

    # Log the list of files found
    logger.debug(f"Got list of files: {files}")

    # Create the email body
    body = "\n".join(files)

    try:
        # Log the email generation
        logger.debug("Generating email")

        # Create the email message
        yag = yagmail.SMTP(EMAIL, PASSWORD)  # Use your email and password
        subject = f"HCSSBOT DATA PULL {datetime.datetime.now()}"

        # Log the email sending
        logger.debug("Sending email")
        yag.send(TARGET_EMAIL, subject, body, attachments=[os.path.join(downloads_folder, file) for file in files])

        logger.info("Email sent")
    
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return  # Optionally return or raise the error

def delete_downloaded_files():

    downloads_folder = "downloads"
    files = os.listdir(downloads_folder)

    for file in files:
        file_path = os.path.join(downloads_folder, file)
        os.remove(file_path)

    # Check if the downloads folder is empty after deletion
    if not os.listdir(downloads_folder):
        logger.debug("Downloads emptied")
