import pandas as pd
import json
import logging
from datetime import datetime
import os

# Ensure the Files directory exists
if not os.path.exists('Files'):
    os.makedirs('Files')

def save_data(data, caller_name, file_type):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"Files/{caller_name}_{timestamp}.{file_type}"

    df = pd.DataFrame(data)

    if file_type == 'xlsx':
        df.to_excel(filename, index=False)
    elif file_type == 'csv':
        df.to_csv(filename, index=False)
    elif file_type == 'json':
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    logging.info(f"Data saved as {file_type.upper()} file: {filename}")
    return filename
