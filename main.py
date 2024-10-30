# main.py

import time
from login import login
from utils_logging import setup_logging, delete_all_screenshots, handle_error, logger
from utils_driver import create_chrome_driver, navigate
from utils_exports import get_exports
from send_email import send_email, delete_downloaded_files

def main():
    
    setup_logging()
    logger.info("Starting main script")
    delete_all_screenshots()

    # Set up the Chrome driver
    driver = create_chrome_driver()

    try:

        # Navigate to the home page
        if not navigate(driver, "https://identity.hcssapps.com/"):
            return  # Exit if navigation failed
        
        # Log in to the website
        if not login(driver):
            return  # Exit if login failed
        
        # Navigate back to the home page
        if not navigate(driver, "https://safety.hcssapps.com/Home/Dashboard"):
            return  # Exit if navigation failed

        # Navigate to Inspections
        if not navigate(driver, "https://safety.hcssapps.com/Inspection/Inspection"):
            return  # Exit if navigation failed

        # Export Inspection Summary
        if not get_exports(driver, "Inspection", "Summary"):
            return  # Exit if exporting failed

        # Export Inspection Item Details
#        if not get_exports(driver, "Inspection", "Details"):
#            return  # Exit if exporting failed
        
        # Navigate back to the home page
#        if not navigate(driver, "https://safety.hcssapps.com/Home/Dashboard"):
#            return  # Exit if navigation failed

        # Navigate to Near Misses
#        if not navigate(driver, "https://safety.hcssapps.com/NearMiss/NearMiss"):
#            return  # Exit if navigation failed

        # Export Near Miss file
#        if not get_exports(driver, "NearMiss", None):
#            return  # Exit if exporting failed

    except Exception as e:
        handle_error(driver, "main_script", e, "An unexpected error occurred")

    finally:
        # Send email with downloaded files
        try:
            # send_email()  # Uncomment if you want to call the send_email function here
            # delete_downloaded_files()  # Uncomment if you want to call the delete_downloaded_files function
            pass
        except Exception as e:
            print(f"Failed to send email or delete files: {str(e)}")
        
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()