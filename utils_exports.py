# utils_exports.py

import logging
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from utils_logging import logger, handle_error
from utils_driver import wait_for_download, DOWNLOAD_DIR  # Import the download path
from utils_inspector import click
from utils_yaml import selectors  # Import the selectors from utils_yaml.py

logger = logging.getLogger(__name__)

def export_data(driver, export_type, file_prefixes):
    try:
        logger.info(f"Starting {export_type} export.")
        
        # Get the appropriate selectors based on export type
        export_button_selector = selectors['second_export_button'][export_type]

        if click(driver, export_button_selector, f"export button for {export_type}"):
            logger.info(f"Clicked the export button for {export_type}. Waiting for download...")

            if wait_for_download(DOWNLOAD_DIR, file_prefixes):
                logger.info(f"{export_type} export completed successfully.")
                return True
            else:
                logger.error(f"{export_type} export failed. No file downloaded within the timeout.")
                return False
        else:
            logger.error(f"Failed to click the export button for {export_type}.")
            return False

    except Exception as e:
        logger.error(f"Error during {export_type} export: {str(e)}")
        handle_error(driver, f"{export_type}_export", e, custom_message="Export failed")
        return False

def get_exports(driver, export_type, export_subtype):
    logger.info(f"Performing {export_type} export.")

    try:
        apply_date_filter(driver)

        file_prefixes = [f"{export_type}_{export_subtype}_export"] if export_subtype else [f"{export_type}_export"]
        export_successful = export_data(driver, export_type, file_prefixes)

        return export_successful

    except Exception as e:
        logger.error(f"Error during {export_type} export: {str(e)}")
        handle_error(driver, "get_export", e, custom_message=f"{export_type} export failed")
        return False

def apply_date_filter(driver):
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Get date filter selectors from YAML
    start_date_input_selector = selectors["date_filter"]["date_input"]
    end_date_input_selector = selectors["date_filter"]["date_input"]  # Adjust if end date input selector is different
    filter_button_selector = selectors["date_filter"]["apply_button"]
    custom_option_selector = selectors["date_filter"]["custom_option"]

    try:
        # Select the 'Custom' option directly
        if click(driver, custom_option_selector, "Custom date option"):
            logger.debug("Selected 'Custom' date range.")
            
            # Click and set the start date
            if click(driver, start_date_input_selector, "start date input"):
                start_date_input = driver.find_element_by_css_selector(start_date_input_selector)
                start_date_input.clear()
                start_date_input.send_keys(start_date)
                logger.debug(f"Start date set to: {start_date}")

            # Click and set the end date
            if click(driver, end_date_input_selector, "end date input"):
                end_date_input = driver.find_element_by_css_selector(end_date_input_selector)
                end_date_input.clear()
                end_date_input.send_keys(end_date)
                logger.debug(f"End date set to: {end_date}")

            # Click the filter button
            if click(driver, filter_button_selector, "filter button"):
                logger.info("Date filter applied successfully.")

    except NoSuchElementException as e:
        logger.error(f"Error applying date filter: {str(e)}")
        handle_error(driver, "apply_date_filter", e, custom_message="Failed to apply date filter")
    except ElementNotInteractableException as e:
        logger.error(f"Element not interactable: {str(e)}")
        handle_error(driver, "apply_date_filter", e, custom_message="Element not interactable when applying date filter")
