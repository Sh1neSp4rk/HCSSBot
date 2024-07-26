import logging
from export_data import export_data
from upload_to_sharepoint import upload_to_sharepoint
from send_email import send_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(upload_to="sharepoint"):
    try:
        file_path = export_data()
        if upload_to == "sharepoint":
            logger.info("Uploading to SharePoint.")
            upload_to_sharepoint(file_path)
        elif upload_to == "email":
            logger.info("Sending via email.")
            send_email(file_path)
        else:
            logger.error("Invalid upload option specified.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(upload_to="sharepoint")  # Change to "email" to send via email instead
