# utils_logging.py

import os
import logging
import datetime
import time

# Initialize the logger
logger = logging.getLogger(__name__)

# Define color codes for console output
COLORS = {
    "DEBUG": "\033[96m",      # Cyan for DEBUG
    "INFO": "\033[94m",       # Light Blue for INFO
    "SUCCESS": "\033[92m",    # Green for SUCCESS
    "WARNING": "\033[93m",    # Yellow for WARNING
    "ERROR": "\033[91m",      # Red for ERROR
    "CRITICAL": "\033[31m",   # Dark Red for CRITICAL
    "RESET": "\033[0m"        # Reset to default
}

# Set your desired timezone here (e.g., 'America/Toronto', 'UTC', etc.)
TIMEZONE = 'America/Toronto'  # Replace with your desired timezone or leave it as None

# Screenshot directory and counter
SCREENSHOT_DIR = "screenshots"
screenshot_counter = 1

# Custom formatter for logging
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Check for "SUCCESS" in the message
        if "SUCCESS" in record.msg:
            color = COLORS["SUCCESS"]
        elif record.levelname in COLORS:
            color = COLORS[record.levelname]
        else:
            color = COLORS["RESET"]  # Default to reset if no match

        # Format the level name with the appropriate color
        level_color = COLORS.get(record.levelname, COLORS["RESET"])
        level_name = f"{level_color}{record.levelname}{COLORS['RESET']}"

        # Format the message with the appropriate color
        message = f"{color}{record.msg}{COLORS['RESET']}"

        # Update the record with the formatted level name
        record.levelname = level_name
        record.msg = message
        
        # Call the parent class's format method
        return super().format(record)

def take_screenshot(driver, step_name):

    global screenshot_counter
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Ensure the screenshot directory exists
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    screenshot_path = f"{SCREENSHOT_DIR}/{screenshot_counter:03d}_{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    logger.info(f"Screenshot taken: {screenshot_path}")  # Updated logging

    screenshot_counter += 1

def delete_all_screenshots():

    if os.path.exists(SCREENSHOT_DIR):
        for filename in os.listdir(SCREENSHOT_DIR):
            file_path = os.path.join(SCREENSHOT_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        logger.debug(f"Deleted all screenshots in {SCREENSHOT_DIR}")  # Updated logging
    else:
        os.makedirs(SCREENSHOT_DIR)
        logger.debug(f"Created screenshot directory: {SCREENSHOT_DIR}")  # Updated logging

def write_ascii_header(log_file):
    header = """
    *******************************************************
    *                NEW SCRIPT EXECUTION                 *
    *******************************************************
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as log:
        log.write(f"\n{header}\n")
        log.write(f"Execution started at: {timestamp}\n")
        log.write("*******************************************************\n")
    return header  # Return the header for use in other functions

def trim_log_file(log_file, header, max_runs=5):
    if not os.path.exists(log_file):
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    # Find all positions of the actual header in the file
    run_indices = [i for i, line in enumerate(lines) if header in line]

    # If we have more runs than the max, trim the file
    if len(run_indices) > max_runs:
        # Keep only the last max_runs sections
        start_index = run_indices[-max_runs]
        lines = lines[start_index:]

        # Write the trimmed log back to the file
        with open(log_file, 'w') as f:
            f.writelines(lines)
        logger.debug(f"Trimmed the log file to keep only the last {max_runs} runs.")

def setup_logging(log_file='logs/app.log'):

    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    logger.debug(f"Log directory created: {log_dir}")

    # Get the header from write_ascii_header
    header = write_ascii_header(log_file)

    # Trim the log file to keep only the last 4 runs before writing the new one
    logger.debug("Trimming log file")
    trim_log_file(log_file, header)
    logger.debug("Log file trimmed")

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        try:
            # File handler for logging to file without color codes
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Console handler for colored output
            console_handler = logging.StreamHandler()
            formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # Set the log level for both handlers to DEBUG
            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.INFO)

            print(f"Logging set up. Logs will be written to: {log_file}")
            logger.debug("This is a debug message for testing.")  # Only log this, not print it
        except Exception as e:
            print(f"Failed to set up logging: {e}")

def handle_error(driver, function_name, error, custom_message=None):

    error_message = f"{custom_message} Error in {function_name}: {str(error)}"
    logger.error(error_message)  # Log the error message with context
    logger.debug(f"Current URL: {driver.current_url}")  # Log the current URL for context
    take_screenshot(driver, "error_screenshot")  # Optional: take a screenshot on error
    return False  # Indicate failure without exiting
