# Tools/data_saver.py
import csv
import json
import logging
import pandas as pd

def save_data(data, file_type):
    logging.debug(f"Saving data as {file_type}")
    if file_type == 'csv':
        save_as_csv(data)
    elif file_type == 'excel':
        save_as_excel(data)
    elif file_type == 'json':
        save_as_json(data)
    else:
        raise ValueError("Unsupported file type. Choose from 'csv', 'excel', or 'json'.")

def save_as_csv(data):
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data[0].keys())  # Write header
        for row in data:
            writer.writerow(row.values())
    logging.info("Data saved as CSV")

def save_as_excel(data):
    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)
    logging.info("Data saved as Excel")

def save_as_json(data):
    with open('output.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    logging.info("Data saved as JSON")
