# utils_driver.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils_logging import log_message

# Constants
DOWNLOAD_DIR = "downloads"
MAX_RETRIES = 3
TIMEOUT = 10  # seconds

def create_chrome_driver():
    """Create a Chrome driver with headless options."""
    log_message("INFO", "Setting up Chrome driver with headless options")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

      # Set the download directory
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(DOWNLOAD_DIR),  # Use absolute path
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    log_message("SUCCESS", "Chrome driver setup complete")

    return driver

def wait_for_download(download_path, file_prefixes, timeout=TIMEOUT):
    """
    Waits for a file to be downloaded in the specified download path.

    :param download_path: Path to the downloads folder.
    :param file_prefixes: List of prefixes for the expected filenames.
    :param timeout: Maximum time to wait for the download in seconds.
    :return: True if the file is downloaded, False otherwise.
    """
    start_time = time.time()
    log_message("INFO", f"Waiting for file download in '{download_path}' with prefixes: {file_prefixes}")
    
    while time.time() - start_time < timeout:
        try:
            # Check for any files in the downloads directory
            for file_prefix in file_prefixes:
                for filename in os.listdir(download_path):
                    if filename.startswith(file_prefix) and filename.endswith('.xlsx'):
                        log_message("SUCCESS", f"File '{filename}' downloaded successfully.")
                        return True
        except Exception as e:
            log_message("ERROR", f"Error checking download directory: {e}")
        
        time.sleep(1)  # Wait before checking again

    log_message("ERROR", "File download timed out.")
    return False

