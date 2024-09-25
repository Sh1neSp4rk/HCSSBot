# main.py

from login import login
from get_inspections import navigate_to_inspections_page, export_inspection_file
from get_nearmisses import navigate_to_nearmisses_page, export_nearmiss_file
from utils_logging import setup_logging, delete_all_screenshots, log_message
from utils_inspector import handle_error, navigate, apply_date_filter  
from utils_driver import create_chrome_driver
from send_email import send_email, delete_downloaded_files  # Import both functions
from datetime import datetime, timedelta
import os

def main():
    setup_logging()
    log_message("INFO", "Starting main script")

    # Delete old screenshots
    delete_all_screenshots()

    # Set up the Chrome driver
    driver = create_chrome_driver()

    try:
        # Log in to the website
        if not login(driver):  # Check if login succeeded
            handle_error(driver, "main_script", None, "Login failed. Exiting script.")
            return

        # Navigate to Inspections
        if not navigate_to_inspections_page(driver):
            handle_error(driver, "main_script", None, "Navigation to inspections failed. Exiting script.")
            return

        # Calculate yesterday and today for date filtering
        today = datetime.now().strftime("%m/%d/%Y")
        yesterday = (datetime.now() - timedelta(1)).strftime("%m/%d/%Y")

        # Apply the date filter for Inspections
        dynamic_yesterday, dynamic_today = apply_date_filter(driver, yesterday, today, "#ResultsTable_info")
        if dynamic_yesterday is None:  # Check if the date filter was applied successfully
            handle_error(driver, "main_script", None, "Date filter application failed for Inspections. Exiting script.")
            return

        # Export Inspection Summary
        if not export_inspection_file(driver, "Summary", "./downloads"):
            handle_error(driver, "main_script", None, "Exporting Inspection Summary failed. Exiting script.")
            return

        # Export Inspection Item Details
        if not export_inspection_file(driver, "Details", "./downloads"):
            handle_error(driver, "main_script", None, "Exporting Inspection Item Details failed. Exiting script.")
            return
        
        # Navigate back to the home page
        navigate(driver, "https://safety.hcssapps.com/Home/Dashboard")

        # Navigate to Near Misses
        if not navigate_to_nearmisses_page(driver):
            handle_error(driver, "main_script", None, "Navigation to near misses failed. Exiting script.")
            return

        # Apply the date filter for Near Misses
        dynamic_yesterday, dynamic_today = apply_date_filter(driver, yesterday, today, "#resultsgrid_1_info")
        if dynamic_yesterday is None:  # Check if the date filter was applied successfully
            handle_error(driver, "main_script", None, "Date filter application failed for Near Misses. Exiting script.")
            return

        # Export Near Miss Summary
        if not export_nearmiss_file(driver, "./downloads"):
            handle_error(driver, "main_script", None, "Exporting Near Miss Summary failed. Exiting script.")
            return

    except Exception as e:
        handle_error(driver, "main_script", e, "An unexpected error occurred")

    finally:
        # Send email with downloaded files
        try:
            send_email()  # Call the send_email function here
            delete_downloaded_files()  # Call the delete_downloaded_files function
        except Exception as e:
            log_message("ERROR", f"Failed to send email or delete files: {str(e)}")
        
        # Close the browser
        driver.quit()

    log_message("SUCCESS", "Main script completed successfully.")

if __name__ == "__main__":
    main()
