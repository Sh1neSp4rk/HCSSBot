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
    """
    Fetches paginated data from the given URL with a progress bar.

    Args:
        url (str): The API URL to request data from.
        headers (dict): The headers to include in the request.
        params (dict): The parameters to include in the request.
        page_size (int): The number of items per page.

    Returns:
        list: A list of all fetched data items.
    """
    logging.info(f"Fetching paginated data from {url} with params {params} and page_size {page_size}")
    all_data = []
    page = 1
    total_pages = None

    # Custom ASCII progress bar format
    # Explanation of the components:
    # '{l_bar}' - Left side of the progress bar (contains the description or label).
    # '{bar}' - The actual progress bar itself, which shows how much progress has been made.
    # '{n_fmt}' - Current number of completed tasks.
    # '{total_fmt}' - Total number of tasks.
    # '{elapsed}' - Time elapsed since the start of the process.
    # '{remaining}' - Estimated time remaining to complete the process.
    # '{rate_fmt}' - Rate of progress (e.g., tasks per second).
    bar_format = (
        '{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {rate_fmt}'
    )
    
    with tqdm(total=1, desc="Fetching data", ascii=True, bar_format=bar_format) as pbar:
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
