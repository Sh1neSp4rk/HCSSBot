#utils_logging.py

import os
import logging
import datetime
import pytz
import sys
import time

# Initialize the logger
logger = logging.getLogger(__name__)

# Define color codes for console output
COLORS = {
    "INFO": "\033[94m",      # Blue
    "SUCCESS": "\033[92m",   # Green
    "WARNING": "\033[93m",   # Yellow
    "ERROR": "\033[91m",     # Red
    "RESET": "\033[0m"       # Reset to default
}

# Set your desired timezone here (e.g., 'America/Toronto', 'UTC', etc.)
TIMEZONE = 'America/Toronto'  # Replace with your desired timezone or leave it as None

# Screenshot directory and counter
SCREENSHOT_DIR = "screenshots"
screenshot_counter = 1

# Custom formatter for logging
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelname == "ERROR":
            record.msg = self.truncate_message(record.msg)
        return super().format(record)

    def truncate_message(self, message):
        if isinstance(message, str) and len(message) > 100:
            return message[:97] + '...'  # Truncate and add ellipsis
        return message

def log_message(message_type, message):
    """Log messages to console with color coding and to the logger."""
    if TIMEZONE:
        local_tz = pytz.timezone(TIMEZONE)
        local_time = datetime.datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    else:
        local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the log entry format
    log_entry = f"{local_time} - {message}"

    # Log to the logger without duplicating console output
    logger_method = {
        "INFO": logger.info,
        "SUCCESS": logger.info,
        "WARNING": logger.warning,
        "ERROR": logger.error,
    }.get(message_type, logger.info)  # Default to info for unknown types

    # Color formatting for console output
    if message_type in COLORS:
        color = COLORS[message_type]
        formatted_message = f"{color}{local_time} [{message_type}] {message}{COLORS['RESET']}"
    else:
        formatted_message = f"{local_time} [{message_type}] {message}"  # Default print for unknown message types

    # Log to the logger
    logger_method(message)  # Log message for file output
    # Print to console
    print(formatted_message)  # Print colored log message to console

def take_screenshot(driver, step_name):
    """Take a screenshot of the current page."""
    global screenshot_counter
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Ensure the screenshot directory exists
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    screenshot_path = f"{SCREENSHOT_DIR}/{screenshot_counter:03d}_{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    log_message("INFO", f"Screenshot taken: {screenshot_path}")
    
    screenshot_counter += 1

def delete_all_screenshots():
    """Delete all screenshots in the screenshots directory."""
    if os.path.exists(SCREENSHOT_DIR):
        for filename in os.listdir(SCREENSHOT_DIR):
            file_path = os.path.join(SCREENSHOT_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        log_message("INFO", f"Deleted all screenshots in {SCREENSHOT_DIR}")
    else:
        os.makedirs(SCREENSHOT_DIR)
        log_message("INFO", f"Created screenshot directory: {SCREENSHOT_DIR}")

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

def trim_log_file(log_file, max_runs=5):
    """Keep only the last max_runs sections of logs, each starting with the ASCII header."""
    if not os.path.exists(log_file):
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    # Find all positions of the ASCII headers in the file
    header = "*******************************************************"
    run_indices = [i for i, line in enumerate(lines) if header in line]

    # If we have more runs than the max, trim the file
    if len(run_indices) > max_runs:
        # Keep only the last max_runs sections
        start_index = run_indices[-max_runs]
        lines = lines[start_index:]

        # Write the trimmed log back to the file
        with open(log_file, 'w') as f:
            f.writelines(lines)
        print(f"Trimmed the log file to keep only the last {max_runs} runs.")

def setup_logging(log_file='logs/app.log'):
    """Set up logging configuration, ensuring only the last 5 runs are kept."""
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    print(f"Log directory created: {log_dir}")

    # Trim the log file to keep only the last 4 runs before writing the new one
    trim_log_file(log_file, max_runs=4)

    write_ascii_header(log_file)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        try:
            file_handler = logging.FileHandler(log_file)
            console_handler = logging.StreamHandler()

            formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.WARNING)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            print(f"Logging set up. Logs will be written to: {log_file}")
            logger.debug("This is a debug message for testing.")  # Only log this, not print it
        except Exception as e:
            print(f"Failed to set up logging: {e}")

def handle_error(driver, function_name, error, custom_message=None, exit_code=1):
    error_message = f"{custom_message} Error: {str(error)}"
    log_message("ERROR", error_message)  # Ensure this uses the log_message function
    take_screenshot(driver, "error_screenshot")  # Optional: take a screenshot on error
    sys.exit(exit_code)  # Exit the script 
