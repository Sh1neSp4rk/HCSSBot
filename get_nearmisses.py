# get_nearmisses.py

from selenium.webdriver.common.by import By
from utils_logging import log_message, take_screenshot
from utils_inspector import handle_error, click, navigate
from utils_driver import wait_for_download

def navigate_to_nearmisses_page(driver):
    """Navigate to the Near Miss page and verify that we are there."""
    dashboard_url = "https://safety.hcssapps.com/Home/Dashboard"
    nearmisses_url = "https://safety.hcssapps.com/NearMiss/NearMiss"

    current_url = driver.current_url
    log_message("INFO", f"Current URL: {current_url}")

    if current_url != dashboard_url:
        log_message("INFO", f"Not on dashboard. Navigating to {dashboard_url}")
        if not navigate(driver, dashboard_url):
            handle_error(driver, "navigate_to_nearmisses_page", None, "Navigation to dashboard failed.")
            return False  # Exit if navigation to dashboard failed

    # Verify navigation to nearmisses
    log_message("INFO", f"Navigating to {nearmisses_url}")
    if not navigate(driver, nearmisses_url, wait_condition=None, element_locator=(By.CSS_SELECTOR, "#resultsgrid_1_info"), element_description="Results Grid Info"):
        error_message = "Navigation to Near Miss page failed."
        log_message("ERROR", error_message)
        handle_error(driver, "navigate_to_nearmisses_page", None, error_message)
        return False  # Exit if navigation to nearmisses failed

    log_message("INFO", "Initial Near Miss page loaded")
    return True  # Successfully navigated

def export_nearmiss_file(driver, downloads_path):
    try:
        # Click the 'Export' button
        log_message("INFO", "Clicking the Export button for Near Miss")
        click(driver, (By.CSS_SELECTOR, "#createEXCELBtn"), "Export Button")

        # Wait for the popup to appear and click the 'Select All' option
        log_message("INFO", "Clicking the 'Select All' option for Near Miss")
        click(driver, (By.CSS_SELECTOR, "#chkselectAll"), "Select All Option")

        # Click the export button to download
        log_message("INFO", "Clicking the Export button to download Near Miss file")
        click(driver, (By.CSS_SELECTOR, "#btnExcelExport"), "Export Button")

        # Wait for the download to complete
        if not wait_for_download(downloads_path, ["NearMiss"]):
            log_message("ERROR", "Near Miss file not downloaded. Exiting function.")
            return None  # Indicate failure

        log_message("SUCCESS", "Near Miss file export initiated and completed successfully.")
        return True  # Indicate success

    except Exception as e:
        handle_error(driver, "export_nearmiss_file", e, "Error occurred while exporting Near Miss file")
        take_screenshot(driver, "error_occurred")  # Capture a screenshot when an error occurs
        return None  # Indicate failure

