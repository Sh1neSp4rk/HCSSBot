# EndpointCalls/safety_get.py
import requests
from datetime import datetime
from EndpointCalls.token_get import get_token
from Tools.logger import setup_main_logger, log_process_start, log_process_completion, log_error

# Set up the main logger
logger = setup_main_logger()

def get_Safety_incidents(limit=0, offset=0):
    url_incidents = "https://api.hcssapps.com/safety/v1/incidents"
    url_incidents_v2 = "https://api.hcssapps.com/safety/v2/incidents"
    token = get_token()
    query_incidents = {
        "limit": limit,
        "offset": offset
    }
    headers = {"Authorization": f"Bearer {token}"}

    start_time = log_process_start(logger, "get_Safety_incidents")
    try:
        # Fetch list of incidents
        response = requests.get(url_incidents, headers=headers, params=query_incidents)
        response.raise_for_status()
        incidents_data = response.json()
        logger.info('Successfully fetched incidents data.')

        if not incidents_data or 'incidents' not in incidents_data:
            logger.warning('No incidents found.')
            return []

        incident_details = []
        for incident in incidents_data['incidents']:
            incident_id = incident.get('id')
            if incident_id:
                query_incidents_v2 = {"excludeForms": "true"}
                response_v2 = requests.get(f"{url_incidents_v2}/{incident_id}", headers=headers, params=query_incidents_v2)
                response_v2.raise_for_status()
                incident_details.append(response_v2.json())
                logger.info(f'Successfully fetched details for incident ID {incident_id}.')

        return incident_details
    except requests.RequestException as e:
        log_error(logger, f"Error fetching incidents data: {e}")
        raise
    finally:
        log_process_completion(logger, "get_Safety_incidents", start_time)

def get_Safety_meetings(start_date=None):
    url = "https://api.hcssapps.com/safety/v1/meetings"
    token = get_token()
    
    query = {}

    # Validate and format start_date if provided
    if start_date:
        try:
            # Ensure start_date is a valid ISO 8601 date format
            datetime.fromisoformat(start_date)  # This will raise ValueError if the format is incorrect
            query["startDate"] = start_date
        except ValueError:
            # Log the error and drop the date parameter
            log_error(logger, f"Invalid date format for start_date: {start_date}. The 'startDate' parameter will be omitted.")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    logger.debug(f"Request URL: {url}")
    logger.debug(f"Request headers: {headers}")
    logger.debug(f"Request parameters: {query}")
    
    start_time = log_process_start(logger, "get_Safety_meetings")
    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        data = response.json()
        logger.info('Successfully fetched meetings data.')
        return data
    except requests.RequestException as e:
        log_error(logger, f"Error fetching meetings data: {e}")
        raise
    finally:
        log_process_completion(logger, "get_Safety_meetings", start_time)
