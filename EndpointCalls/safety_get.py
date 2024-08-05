import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='Logs/safety_get.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_incidents(token, modified_after=None, created_after=None, incident_date_after=None, incident_date_before=None, limit=0, offset=0):
    url = "https://api.hcssapps.com/safety/v1/incidents"
    query = {
        "modifiedAfterUtc": modified_after,
        "createdAfterUtc": created_after,
        "incidentDateAfterUtc": incident_date_after,
        "incidentDateBeforeUtc": incident_date_before,
        "limit": limit,
        "offset": offset
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        data = response.json()
        logging.info('Successfully fetched incidents data.')
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching incidents data: {e}")
        raise

def get_incident_details(token, incident_id):
    url = f"https://api.hcssapps.com/safety/v2/incidents/{incident_id}"
    query = {"excludeForms": "true"}
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        data = response.json()
        logging.info(f'Successfully fetched details for incident ID {incident_id}.')
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching details for incident ID {incident_id}: {e}")
        raise

def get_meetings(token, job_id=None, recorder_id=None, business_unit_id=None, employee_id=None, start_date=None, end_date=None, skip=0, take=0):
    url = "https://api.hcssapps.com/safety/v1/meetings"
    query = {
        "jobId": job_id,
        "recorderId": recorder_id,
        "businessUnitId": business_unit_id,
        "employeeId": employee_id,
        "startDate": start_date,
        "endDate": end_date,
        "skip": skip,
        "take": take
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        data = response.json()
        logging.info('Successfully fetched meetings data.')
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching meetings data: {e}")
        raise

if __name__ == "__main__":
    token = "YOUR_ACCESS_TOKEN"  # Replace with your actual token
    try:
        # Example usage
        incidents_data = get_incidents(token, limit=10)
        print(incidents_data)

        if incidents_data:
            first_incident_id = incidents_data.get('incidents', [])[0].get('id')
            if first_incident_id:
                details = get_incident_details(token, first_incident_id)
                print(details)

        meetings_data = get_meetings(token, job_id="example-job-id")
        print(meetings_data)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
