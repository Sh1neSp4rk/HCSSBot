# utils_inspector.py

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from utils_logging import logger, log_args  # Import the logger instance directly

def click(driver, locator, description):
    try:
        # Inspect the element before clicking
        element = inspect(driver, locator, description)
        if element:
            element.click()
            logger.debug(f"Successfully clicked {description}")
            return True  # Return True if click is successful
        else:
            logger.warning(f"{description} could not be inspected, cannot click.")
            return False

    except Exception as e:
        logger.error(f"Error clicking {description}: {str(e)}")
        return False

@log_args
def inspect(driver, locator=None, description=None, expected_url=None, timeout=2, wait_between_retries=0.25, wait_for_disappear=False):
    if expected_url is not None:
        # If an expected URL is provided, check the current URL
        start_time = time.time()  # Record the start time
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                logger.error(f"Current URL could not be checked after {timeout} seconds.")
                return False  # Return False if the max duration is exceeded
            
            current_url = driver.current_url
            if current_url == expected_url:
                logger.debug(f"Successfully navigated to the expected URL: {current_url}")
                return True  # Successfully navigated to the expected URL
            
            logger.warning(f"Current URL '{current_url}' does not match expected URL '{expected_url}'. Retrying...")
            time.sleep(wait_between_retries)
        
    else:
        previous_displayed = None
        previous_enabled = None
        start_time = time.time()  # Record the start time

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                logger.error(f"{description} could not be inspected after {timeout} seconds.")
                return None  # Return None if the max duration is exceeded
            
            time.sleep(wait_between_retries)
            try:
                # Log the locator being used
                logger.debug(f"Attempting to find element for {description} using locator: {locator}")
                
                 # If we are waiting for the element to disappear
                if wait_for_disappear:
                    # Wait until the element is no longer present
                    WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(locator))
                    logger.debug(f"{description} has disappeared.")
                    return True  # Return True if the element has disappeared
                
                # Wait for the presence of the element
                element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
                # Wait for the element to be stable (not stale)
                WebDriverWait(driver, timeout).until_not(EC.staleness_of(element))

                # Check the current state of the element
                current_displayed = element.is_displayed()
                current_enabled = element.is_enabled()

                # Log the inspection result
                logger.debug(f"Inspecting {description}: Tag={element.tag_name}, Displayed={current_displayed}, Enabled={current_enabled}")

                if current_displayed and current_enabled:
                    return element  # Successfully inspected element

                if not current_displayed:
                    logger.warning(f"{description} is not visible.")
                if not current_enabled:
                    logger.warning(f"{description} is not enabled.")

                logger.debug("Retrying...")

            except StaleElementReferenceException:
                logger.warning(f"{description} is stale.")
                logger.debug("Retrying...")
                continue  # Retry if stale

            except NoSuchElementException:
                logger.warning(f"{description} not found.")
                logger.debug("Retrying...")
                continue  # Retry if not found

            except TimeoutException:
                logger.error(f"Timeout while waiting for {description} to appear.")
                return None  # Return None if timeout occurs

            except Exception as e:
                logger.error(f"Unexpected error while inspecting {description}: {str(e)}")
                return None