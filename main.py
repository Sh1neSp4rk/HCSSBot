import asyncio
import aiohttp
import os
from Tools.logger import setup_logger, log_process_start, log_process_completion, log_error
from Tools.rate_limiter import RateLimiter
from Tools.progress_bars import fetch_paginated_data_with_progress
from Tools.data_saver import save_data
from Tools.cleanup_files import cleanup_files
from Tools.email_sender import send_email

# Import all functions from EndpointCalls
from EndpointCalls import (
    get_business_units,
    get_fuel_costs,
    get_work_order_costs,
    get_work_order_details,
    get_custom_fields,
    get_custom_field_categories,
    get_heavybidestimates_business_units,
    get_heavybidestimates_partitions,
    get_heavyjob_data,
    get_safety_data,
    get_accounting_templates,
    get_jobs,
    get_equipment,
    get_employees,
    fetch_skills,
    fetch_employee_skills,
    get_all_skills,
    get_all_employee_skills,
    get_equipment as get_telematics_equipment,
    get_token,
)

async def main():
    logger = setup_logger()

    # Fetch environment variables
    file_type = "xlsx"
    recipient_email = os.getenv("TARGET_EMAIL")
    rate_limit_percentage = 0.8
    
    rate_limiter = RateLimiter(rate_limit_percentage)
    
    try:
        log_process_start(logger, "Data Fetching")
        
        # Example of running one of the _get functions
        data = get_business_units(file_type)
        filename = save_data(data, "business_units", file_type)
        
        log_process_completion(logger, "Data Fetching")
        
        log_process_start(logger, "Sending Email")
        send_email([filename], recipient_email)
        log_process_completion(logger, "Sending Email")

    except Exception as e:
        log_error(logger, f"An error occurred: {e}")

    finally:
        cleanup_files("Files")

if __name__ == "__main__":
    asyncio.run(main())
