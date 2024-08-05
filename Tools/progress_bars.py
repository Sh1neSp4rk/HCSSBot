# Tools/progress_bars.py
import requests
from tqdm import tqdm
from Tools.logger import log_error, setup_main_logger

# Set up logging
logger = setup_main_logger()

def fetch_data_with_progress(url, headers, params=None):
    logger.info(f"Sending request to {url} with params {params}")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log_error(logger, f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        log_error(logger, f"An error occurred: {e}")
        raise
    logger.info(f"Received response with status code {response.status_code}")
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
    logger.info(f"Fetching paginated data from {url} with params {params} and page_size {page_size}")
    all_data = []
    page = 1
    total_pages = None

    # Custom ASCII progress bar format
    bar_format = (
        '{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {rate_fmt}'
    )
    
    with tqdm(total=1, desc="Fetching data", ascii=True, bar_format=bar_format) as pbar:
        while True:
            params.update({
                "page": page,
                "pageSize": page_size
            })
            try:
                response = fetch_data_with_progress(url, headers, params)
                data = response.json()
            except Exception as e:
                log_error(logger, f"Failed to fetch paginated data: {e}")
                break

            if total_pages is None:
                total_pages = data.get('totalPages', 1)
                pbar.total = total_pages

            all_data.extend(data.get('results', []))
            pbar.update(1)

            if page >= total_pages:
                break
            page += 1

    return all_data
