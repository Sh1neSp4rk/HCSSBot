# utils_driver.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils_logging import logger, handle_error

# Constants
DOWNLOAD_DIR = "downloads"
TIMEOUT = 10  # seconds

def log_browser_versions():

    chrome_version = os.popen('google-chrome --version').read().strip()
    chromedriver_version = os.popen('chromedriver --version').read().strip()
    logger.debug(f"Installed Google Chrome version: {chrome_version}")
    logger.debug(f"Installed ChromeDriver version: {chromedriver_version}")

def create_chrome_driver():

    logger.debug("Setting up Chrome driver with headless options")

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
    logger.debug("Chrome driver setup complete")
    
    # Log versions after driver creation
    log_browser_versions()

    return driver

def navigate(driver, url):

    try:
        driver.get(url)
        logger.debug(f"Navigating to {url}")

        # Check if the current URL contains the target URL
        if url not in driver.current_url:
            logger.warning(f"Navigation failed: expected URL to contain '{url}', but got '{driver.current_url}'.")
            return False  # Indicate failure

        logger.info(f"Successfully navigated to {url}.")
        return True  # Indicate success

    except Exception as e:
        handle_error(driver, "navigate", e, f"Error occurred while navigating to {url}")
        return False  # Indicate failure

def wait_for_download(download_path, timeout=TIMEOUT):
    start_time = time.time()
    logger.info(f"Waiting for file download in '{download_path}'.")

    while time.time() - start_time < timeout:
        try:
            # Check for any xlsx files in the downloads directory
            for filename in os.listdir(download_path):
                if filename.endswith('.xlsx'):
                    logger.info(f"File '{filename}' downloaded successfully.")
                    return True
        except Exception as e:
            logger.error(f"Error checking download directory: {e}")

        time.sleep(1)  # Wait before checking again

    logger.error("File download timed out.")
    return False