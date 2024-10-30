# utils_yaml.py

import yaml
from utils_logging import logger 

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            logger.info(f"Successfully loaded YAML file: {file_path}")  # Log successful load
            return data
    except FileNotFoundError:
        logger.error(f"Error: The file {file_path} was not found.")  # Log file not found
        return None
    except yaml.YAMLError as exc:
        logger.error(f"Error in YAML file: {exc}")  # Log YAML parsing error
        return None

# Load selectors from the paths.yaml
selectors = load_yaml('paths.yaml')
