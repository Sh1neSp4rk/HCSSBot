# utils_exports.py

from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils_logging import logger, handle_error, log_args
from utils_driver import wait_for_download
from utils_inspector import click
from utils_yaml import selectors

@log_args
def get_export(driver, report_type):
    logger.info(f"Performing {report_type} export.")
    
    locators = {
        'url': (By.CSS_SELECTOR, selectors[report_type]['url']),
        'date_field': (By.CSS_SELECTOR, selectors[report_type]['custom_date_field']['selector']),
        'custom_option': (By.CSS_SELECTOR, selectors[report_type]['custom_date_field']['custom_option']),
        'start_date': (By.CSS_SELECTOR, selectors[report_type]['date']['start']),
        'end_date': (By.CSS_SELECTOR, selectors[report_type]['date']['end']),
        'apply_button': (By.CSS_SELECTOR, selectors[report_type]['apply_button']),
        'loader': (By.CSS_SELECTOR, selectors[report_type]['loader']),
        'first_export': (By.CSS_SELECTOR, selectors[report_type]['export_buttons']['first']),
        'second_export': (By.CSS_SELECTOR, selectors[report_type]['export_buttons']['second']),
        'selection': (By.CSS_SELECTOR, selectors[report_type]['export_buttons']['selection']),
        'select_all': (By.CSS_SELECTOR, selectors[report_type]['select_all']),
    }
    
    # Apply date filter before exporting
    if not apply_date_filter(driver, locators):
        return False

    # Export data based on report type
    return export_data(driver, locators)

@log_args
def apply_date_filter(driver, locators):
    end_date = datetime.now().strftime("%m/%d/%Y")
    start_date = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")

    try:
        if click(driver, locators['date_field'], "date range dropdown"):
            logger.debug("Date range dropdown clicked.")

            if click(driver, locators['custom_option'], "Custom date option"):
                logger.debug("Selected 'Custom' date range.")

            start_date_input = driver.find_element(*locators['start_date'])
            start_date_input.clear()
            start_date_input.send_keys(start_date)
            logger.info(f"Start date set to: {start_date}")

            end_date_input = driver.find_element(*locators['end_date'])
            end_date_input.clear()
            end_date_input.send_keys(end_date)
            logger.info(f"End date set to: {end_date}")

            if click(driver, locators['apply_button'], "filter button"):
                logger.info("Date filter applied successfully.")
                
                # Wait for loader to indicate data load
                wait_for_loader(driver, locators['loader'])
                return True

    except (NoSuchElementException, ElementNotInteractableException) as e:
        logger.error(f"Error applying date filter: {str(e)}")
        handle_error(driver, "apply_date_filter", e, custom_message="Failed to apply date filter")

    return False

@log_args
def export_data(driver, report_selectors):
    logger.debug(f"Exporting data for {report_selectors}")

    # Click the first export button to open the dropdown
    logger.debug("Clicking first export button to select export type.")
    click(driver, report_selectors['export_buttons']['first'], "First export button")

    # Conditionally select the appropriate export type if 'selection' is present
    if report_selectors['export_buttons'].get('selection'):
        logger.debug("Selecting specific export option.")
        click(driver, report_selectors['export_buttons']['selection'], "Export selection")

    # Select all options from the new dropdown
    logger.debug("Selecting all options for export.")
    click(driver, report_selectors['select_all'], "Select all options for export")

    # Click the second export button to start the download
    logger.debug("Clicking second export button to initiate download.")
    click(driver, report_selectors['export_buttons']['second'], "Second export button")

    # Wait for download to complete if necessary (you can adjust the timeout)
    download_path = "your/download/path"  # Set your actual download path
    file_prefixes = ["expected_prefix"]  # Specify the expected file prefixes
    wait_for_download(download_path, file_prefixes)

    return True

def wait_for_loader(driver, loader_locator, timeout=10):
    """Wait for the loader to appear and disappear, indicating a data load."""
    try:
        # Wait for loader to appear
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(loader_locator))
        logger.debug("Loader appeared, waiting for it to disappear.")
        
        # Wait for loader to disappear
        WebDriverWait(driver, timeout).until_not(EC.visibility_of_element_located(loader_locator))
        logger.debug("Loader disappeared, data load complete.")

    except TimeoutException:
        logger.warning("Timeout waiting for loader to disappear.")
