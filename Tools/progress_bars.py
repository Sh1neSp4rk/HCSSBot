# Tools/progress_bars.py
import requests
from tqdm import tqdm
import logging

def fetch_data_with_progress(url, headers, params=None):
    logging.info(f"Sending request to {url} with params {params}")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    logging.info(f"Received response with status code {response.status_code}")
    return response

def fetch_paginated_data_with_progress(url, headers, params, page_size=50):
    logging.info(f"Fetching paginated data from {url} with params {params} and page_size {page_size}")
    all_data = []
    page = 1
    total_pages = None

    with tqdm(total=1, desc="Fetching data") as pbar:
        while True:
            params.update({
                "page": page,
                "pageSize": page_size
            })
            response = fetch_data_with_progress(url, headers, params)
            data = response.json()

            if total_pages is None:
                total_pages = data.get('totalPages', 1)
                pbar.total = total_pages

            all_data.extend(data.get('results', []))
            pbar.update(1)

            if page >= total_pages:
                break
            page += 1

    return all_data
