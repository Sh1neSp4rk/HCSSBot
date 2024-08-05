# Tools/progress_bars.py
import requests
from tqdm import tqdm
import logging

status_logger = logging.getLogger('status_logger')

def fetch_data_with_progress(url, headers, params=None):
    logging.info(f"Sending request to {url} with params {params}")
    status_logger.info(f"Sending request to {url} with params {params}")
    response = requests.get(url, headers=headers, params=params)
    status_logger.info(f"Received response with status code {response.status_code}")
    response.raise_for_status()  # Raise an exception for HTTP errors
    logging.info(f"Received response with status code {response.status_code}")
    return response

def fetch_paginated_data_with_progress(url, headers, business_unit_id, page_size=50):
    logging.info(f"Fetching paginated data from {url} with business_unit_id {business_unit_id} and page_size {page_size}")
    status_logger.info(f"Fetching paginated data from {url} with business_unit_id {business_unit_id} and page_size {page_size}")
    all_data = []
    page = 1
    total_pages = None

    with tqdm(total=1, desc="Fetching data") as pbar:  # Initialize with total=1, will update later
        while True:
            params = {
                "page": page,
                "pageSize": page_size,
                "businessUnitId": business_unit_id
            }
            response = fetch_data_with_progress(url, headers, params)
            data = response.json()

            if total_pages is None:
                total_pages = data.get('totalPages', 1)
                pbar.total = total_pages  # Update the total number of pages in the progress bar

            all_data.extend(data.get('results', []))
            pbar.update(1)  # Increment the progress bar

            if page >= total_pages:
                break
            page += 1

    return all_data
