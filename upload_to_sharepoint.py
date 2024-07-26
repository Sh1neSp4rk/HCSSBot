import os
import logging
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_to_sharepoint(file_path):
    sharepoint_url = "https://yourcompany.sharepoint.com/sites/your_site"
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    logger.info("Connecting to SharePoint.")
    ctx = ClientContext(sharepoint_url).with_credentials(ClientCredential(client_id, client_secret))
    target_folder_url = "/sites/your_site/Shared Documents"

    with open(file_path, "rb") as content_file:
        file_content = content_file.read()
    logger.info(f"Uploading file to SharePoint: {file_path}")
    ctx.web.get_folder_by_server_relative_url(target_folder_url).upload_file(os.path.basename(file_path), file_content).execute_query()
    logger.info("File uploaded successfully.")
