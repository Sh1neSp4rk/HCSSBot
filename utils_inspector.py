# utils_inspector.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from utils_logging import log_message, handle_error


def click(driver, locator, description, timeout=10):
    """Attempt to click an element after inspecting it."""
    try:
        # Inspect the element before clicking
        element = inspect(driver, locator, description, retries=1, timeout=timeout)
        if element:
            element.click()
            log_message("SUCCESS", f"Successfully clicked {description}")
            return True  # Return True if click is successful
        else:
            log_message("INFO", f"{description} could not be inspected, cannot click.")
            return False

    except Exception as e:
        handle_error(driver, description, e, f"Error clicking {description}")
        return False

def inspect(driver, locator, description, retries=3, timeout=10, wait_between_retries=2):
    """Inspect an element, ensuring it is not stale and retrying if necessary."""
    previous_displayed = None
    previous_enabled = None

    for attempt in range(retries):
        time.sleep(wait_between_retries)
        try:
            # Wait for the presence of the element
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
            # Wait for the element to be stable (not stale)
            WebDriverWait(driver, timeout).until_not(EC.staleness_of(element))

            # Check the current state of the element
            current_displayed = element.is_displayed()
            current_enabled = element.is_enabled()

            # Log the inspection result only if it has changed
            if previous_displayed is None or previous_displayed != current_displayed:
                log_message("INFO", f"Inspecting {description}: Tag={element.tag_name}, Displayed={current_displayed}, Enabled={current_enabled}")
            if current_displayed:
                previous_displayed = current_displayed
            if current_enabled:
                previous_enabled = current_enabled

            # Check for visibility and enabled state to decide if we should retry
            if not current_displayed:
                log_message("INFO", f"{description} is not visible.")
            if not current_enabled:
                log_message("INFO", f"{description} is not enabled.")

            if current_displayed and current_enabled:
                return element  # Successfully inspected element

            log_message("INFO", "Retrying...")
            continue  # Retry if not visible or enabled

        except StaleElementReferenceException:
            log_message("INFO", f"{description} is stale.")
            log_message("INFO", "Retrying...")
            continue  # Retry if stale

        except NoSuchElementException:
            log_message("INFO", f"{description} not found.")
            log_message("INFO", "Retrying...")
            continue  # Retry if not found

        except Exception as e:
            log_message("ERROR", f"Unexpected error while inspecting {description}: {str(e)}")
            handle_error(driver, description, e, f"Error inspecting {description}")
            return None

    log_message("ERROR", f"{description} could not be inspected after {retries} attempts.")
    return None  # Return None if all retries fail

def navigate(driver, url, wait_condition=None, retries=3, wait_time=2, element_locator=None, element_description="target element"):
    """Navigate to a specific URL and verify that the page has loaded using a condition or element verification."""
    try:
        driver.get(url)
        log_message("INFO", f"Navigating to {url}")

        if wait_condition or element_locator:
            for attempt in range(retries):
                try:
                    log_message("INFO", f"Attempt {attempt + 1} for verifying page load")

                    if wait_condition:
                        WebDriverWait(driver, 10).until(wait_condition)
                        log_message("SUCCESS", f"Successfully verified page load condition for {url}")
                        return True  # Successfully navigated and verified

                    # If a specific element is provided, verify its presence
                    if element_locator:
                        inspect(driver, element_locator, element_description)
                        log_message("SUCCESS", f"Successfully verified presence of {element_description}")
                        return True

                except TimeoutException:
                    log_message("WARNING", f"Page not loaded yet, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

            log_message("ERROR", f"Failed to verify page load after {retries} attempts")
            return False  # Failed to verify

        return True  # No wait condition or element provided, just navigated successfully

    except Exception as e:
        handle_error(driver, "navigate", e, f"Error occurred while navigating to {url}")
        return False  # Indicate failure
    
def apply_date_filter(driver, start_date, end_date, result_info_selector):
    """Set the custom date range filter and apply it."""
    try:
        # Set custom date range (start_date to end_date)
        log_message("INFO", f"Setting date range: {start_date} to {end_date}")

        # Select 'Custom' in the dropdown
        inspect(driver, (By.CSS_SELECTOR, "#dateRangeSelect"), "Date Range Select")
        click(driver, (By.CSS_SELECTOR, "#dateRangeSelect option[value='Custom']"), "Custom Option")

        # Set the 'From' date
        inspect(driver, (By.CSS_SELECTOR, "#filterdatebeginput"), "From Date Input").clear()
        inspect(driver, (By.CSS_SELECTOR, "#filterdatebeginput"), "From Date Input").send_keys(start_date)

        # Set the 'To' date
        inspect(driver, (By.CSS_SELECTOR, "#filterdateendinput"), "To Date Input").clear()
        inspect(driver, (By.CSS_SELECTOR, "#filterdateendinput"), "To Date Input").send_keys(end_date)

        log_message("INFO", "Date range set")

        # Click the 'Apply' button
        inspect(driver, (By.CSS_SELECTOR, "#applyButton"), "Apply Button")
        click(driver, (By.CSS_SELECTOR, "#applyButton"), "Apply Button")

        # Check the updated number of entries
        updated_entries_text = inspect(driver, (By.CSS_SELECTOR, result_info_selector), "Results Grid Info").text
        updated_entries_count = int(updated_entries_text.split("of")[-1].strip().split()[0])
        log_message("INFO", f"Updated number of entries: {updated_entries_count}")

        # Exit if there are no entries
        if updated_entries_count == 0:
            log_message("INFO", "No entries found after applying the date filter. No data to export.")
            return None, None  # Indicate failure

        log_message("SUCCESS", "Date filter applied successfully")

        return start_date, end_date  # Return the date range

    except Exception as e:
        handle_error(driver, "apply_date_filter", e, "Error occurred while applying date filter")
        return None, None  # Indicate failure
