# get_inspections.py

from selenium.webdriver.common.by import By
from utils_logging import log_message, take_screenshot
from utils_inspector import handle_error, click, navigate
from utils_driver import wait_for_download

def navigate_to_inspections_page(driver):
    """Navigate to the Inspections page and verify that we are there."""
    dashboard_url = "https://safety.hcssapps.com/Home/Dashboard"
    inspections_url = "https://safety.hcssapps.com/Inspection/Inspection"

    current_url = driver.current_url
    log_message("INFO", f"Current URL: {current_url}")

    if current_url != dashboard_url:
        log_message("INFO", f"Not on dashboard. Navigating to {dashboard_url}")
        if not navigate(driver, dashboard_url):
            handle_error(driver, "navigate_to_inspections_page", None, "Navigation to dashboard failed.")
            return False  # Exit if navigation to dashboard failed

    # Verify navigation to inspections
    if not navigate(driver, inspections_url, wait_condition=None, element_locator=(By.CSS_SELECTOR, "#InspectionHistoryResultsGrid"), element_description="Inspection History Results Grid"):
        error_message = "Navigation to inspections failed."
        log_message("ERROR", error_message)
        handle_error(driver, "navigate_to_inspections_page", None, error_message)
        return False  # Exit if navigation to inspections failed

    log_message("INFO", "Initial inspections page loaded")
    return True  # Successfully navigated

def export_inspection_file(driver, file_type, downloads_path):
    try:
        # Click the 'Export' button to reveal the dropdown
        log_message("INFO", "Clicking the Export button to reveal options")
        click(driver, (By.CSS_SELECTOR, "span.dropdown.exportBtn.btn-group > button"), "Export Button")

        # Click the appropriate inspection export option
        log_message("INFO", f"Clicking the option to export Inspection {file_type}")
        click(driver, (By.CSS_SELECTOR, f"#create{file_type}Excel"), f"Inspection {file_type}")

        # Click the 'Select All' option
        log_message("INFO", f"Clicking 'Select All' for {file_type}")
        click(driver, (By.CSS_SELECTOR, f"#chk{file_type}SelectAll"), "Select All Option")

        # Click the final export button
        log_message("INFO", f"Clicking the Export button for {file_type}")
        click(driver, (By.CSS_SELECTOR, f"#btn{file_type}Export"), f"Export Button")

        log_message("SUCCESS", "File export initiated")

        # Handle the download check based on file_type
        if file_type == "Summary":
            prefix = "InspectionSummaryReport"
        elif file_type == "Details":
            prefix = "InspectionItemDetails"
        else:
            log_message("ERROR", "Invalid file_type provided. Exiting function.")
            return None  # Indicate failure

        # Wait for the download to complete
        if not wait_for_download(downloads_path, [prefix]):
            log_message("ERROR", f"{prefix} Inspection file not downloaded. Exiting function.")
            return None  # Indicate failure

        return True  # Indicate success

    except Exception as e:
        handle_error(driver, f"export_inspection_{file_type}", e, f"Error occurred while exporting inspection {file_type}")
        take_screenshot(driver, "error_occurred")  # Capture a screenshot when an error occurs
        return None  # Indicate failure


