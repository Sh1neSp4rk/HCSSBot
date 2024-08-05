# Tools/logger.py
import logging
import os

# Configure logger
def setup_logger(log_dir='Logs', log_filename='data_fetch.log'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_path = os.path.join(log_dir, log_filename)
    
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

# Function to log the start of a process
def log_process_start(logger, process_name):
    logger.info(f"Starting {process_name}")

# Function to log the completion of a process
def log_process_completion(logger, process_name):
    logger.info(f"{process_name} completed successfully")

# Function to log errors
def log_error(logger, error_message):
    logger.error(error_message)
