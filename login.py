# login.py

import os
import traceback
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils_inspector import inspect, click, handle_error, navigate
from utils_logging import log_message, take_screenshot

# Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv("HCSS_USERNAME")
PASSWORD = os.getenv("HCSS_PASSWORD")

def login(driver):
    safetydash_url = "https://safety.hcssapps.com/Home/Dashboard"
    
    # Locators
    locators = {
        "username": (By.CSS_SELECTOR, "input[name='username']"),
        "password": (By.CSS_SELECTOR, "input[name='password']"),
        "next_button": (By.CSS_SELECTOR, "button.login-button[type='submit']"),
        "login_button": (By.CSS_SELECTOR, "button[type='submit']"),
        "dashboard": (By.CSS_SELECTOR, "div.Page-headerInnerWrapper")
    }

    log_message("INFO", "Attempting to log in")
    
    # Navigate to the dashboard URL
    if not navigate(driver, safetydash_url):
        handle_error(driver, "login", None, "Failed to navigate to the dashboard URL.")
        return False  # Return False on failure

    try:
        # Inspect and populate username
        log_message("INFO", "Locating and populating username field")
        if not inspect(driver, locators["username"], "Username field"):
            handle_error(driver, "login", None, "Failed to inspect username field.")
            return False  # Return False on failure

        driver.find_element(*locators["username"]).send_keys(USERNAME)

        # Click Next button
        log_message("INFO", "Clicking next button")
        if not click(driver, locators["next_button"], "Next button"):
            handle_error(driver, "login", None, "Failed to click next button.")
            return False  # Return False on failure

        # Wait for password field and inspect it
        log_message("INFO", "Waiting for and inspecting password field")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locators["password"]))
        if not inspect(driver, locators["password"], "Password field"):
            handle_error(driver, "login", None, "Failed to inspect password field.")
            return False  # Return False on failure

        driver.find_element(*locators["password"]).send_keys(PASSWORD)

        # Click Login button
        log_message("INFO", "Clicking login button")
        if not click(driver, locators["login_button"], "Login button"):
            handle_error(driver, "login", None, "Failed to click login button.")
            return False  # Return False on failure

        # Confirm successful login
        log_message("INFO", "Confirming login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locators["dashboard"]))
        current_url = driver.current_url
        log_message("INFO", f"Current URL: {current_url}")
        
        if current_url == safetydash_url:
            log_message("SUCCESS", "Successfully navigated to the dashboard")
            return True  # Return True on success
        else:
            handle_error(driver, "login", None, f"Expected URL: {safetydash_url}, but got: {current_url}")
            return False  # Return False on failure

    except (StaleElementReferenceException, ElementNotInteractableException) as e:
        handle_error(driver, "login", e, "Element issue during login")
        return False  # Return False on failure

    except Exception as e:
        error_info = traceback.format_exc()
        log_message("ERROR", f"An unexpected error occurred in login: {error_info}")
        handle_error(driver, "login", e, "An unexpected error occurred during login")
        return False  # Return False on failure
