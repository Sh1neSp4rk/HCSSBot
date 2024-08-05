# Tools/logger.py
import logging
import os
from datetime import datetime

def setup_main_logger(log_dir='Logs', log_filename='data_fetch.log'):
    """
    Set up the main logger for overall actions.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_path = os.path.join(log_dir, log_filename)
    
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

def setup_function_logger(log_dir='Logs', log_filename='function_calls.log'):
    """
    Set up the logger for function calls.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_path = os.path.join(log_dir, log_filename)
    
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

def log_process_start(logger, process_name):
    logger.info(f"Starting {process_name}")

def log_process_completion(logger, process_name):
    logger.info(f"{process_name} completed successfully")

def log_error(logger, error_message):
    logger.error(error_message)

def log_function_call(logger, function_name, start_time):
    """
    Log function call details including start and completion times.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"Function {function_name} started at {start_time}")

def log_function_completion(logger, function_name, start_time):
    """
    Log function completion details with the elapsed time.
    """
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elapsed_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    logger.info(f"Function {function_name} completed at {end_time}. Elapsed time: {elapsed_time}")

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def set_last_successful_date(logger, process_name):
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    logger.info(f"{process_name} - Last Successful Date: {timestamp}")

def get_last_successful_date_from_log(logger, process_name):
    log_path = os.path.join('Logs', f'{process_name}_get.log')
    if not os.path.exists(log_path):
        return None

    with open(log_path, 'r') as file:
        for line in reversed(file.readlines()):
            if f"{process_name} - Last Successful Date:" in line:
                return line.split(': ')[-1].strip()
    return None
