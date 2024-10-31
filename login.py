# login.py

import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from utils_inspector import inspect, click
from utils_logging import logger, handle_error
from utils_yaml import selectors

# Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv("HCSS_USERNAME")
PASSWORD = os.getenv("HCSS_PASSWORD")


def login(driver):
    logger.debug("Entering login function")

    # Define locators using a dictionary
    locators = {
        'username': (By.CSS_SELECTOR, selectors['login']['username']),
        'password': (By.CSS_SELECTOR, selectors['login']['password']),
        'next_button': (By.CSS_SELECTOR, selectors['login']['next_button']),
        'login_button': (By.CSS_SELECTOR, selectors['login']['login_button']),
        'error_message': (By.CSS_SELECTOR, selectors['login']['error_message']),
    }

    logger.info("Attempting to log in")

    # Inspect and populate username
    logger.debug("Inspecting username field")
    if not inspect(driver, locators['username'], "Username field"):
        handle_error(driver, "login", Exception("Username field not found"), "Failed to inspect username field")
        return False

    logger.debug("Entering username")
    start_time = time.time()
    driver.find_element(*locators['username']).send_keys(USERNAME)
    logger.info(f"Username entered successfully. Time taken: {time.time() - start_time:.2f} seconds")

    # Click Next button
    logger.debug("Clicking Next button")
    if not click(driver, locators['next_button'], "Next button"):
        handle_error(driver, "login", None, "Failed to click next button")
        return False

    # Wait for password field and inspect it
    logger.debug("Inspecting password field")
    if not inspect(driver, locators['password'], "Password field"):
        handle_error(driver, "login", None, "Failed to inspect password field")
        return False

    logger.debug("Entering password")
    start_time = time.time()
    driver.find_element(*locators['password']).send_keys(PASSWORD)
    logger.info(f"Password entered successfully. Time taken: {time.time() - start_time:.2f} seconds")

    # Click Login button
    logger.debug("Clicking Login button")
    if not click(driver, locators['login_button'], "Login button"):
        handle_error(driver, "login", None, "Failed to click login button")
        return False

    # Check for error message
    if driver.find_elements(*locators['error_message']):
        error_message = driver.find_element(*locators['error_message']).text
        logger.error(f"Login failed: {error_message}")
        return False

    logger.info("Login successful")
    logger.debug("Exiting login function")
    return True  # Return True on successful login