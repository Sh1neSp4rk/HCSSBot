import argparse
import asyncio
import os
from Tools.logger import setup_logger, log_process_start, log_process_completion, log_error
from Tools.rate_limiter import RateLimiter
from Tools.data_saver import save_data
from Tools.cleanup_files import cleanup_files
from Tools.email_sender import send_email

# Import all functions from EndpointCalls
from EndpointCalls import (
    get_EquipmentE360_business_units,
    get_EquipmentE360_fuel_costs,
    get_EquipmentE360_work_order_costs,
    get_EquipmentE360_work_order_details,
    get_EquipmentE360_custom_fields,
    get_EquipmentE360_custom_field_categories,
    get_HeavyBidEstimates_business_units,
    get_HeavyBidEstimates_partitions,
    get_HeavyJob_businessunits,
    get_HeavyJob_jobs,
    get_HeavyJob_jobcosts,
    get_HeavyJob_costcodes,
    get_HeavyJob_jobemployees,
    get_HeavyJob_jobequipment,
    get_HeavyJob_jobmaterials,
    get_HeavyJob_materials,
    get_HeavyJob_timecards,
    get_HeavyJob_user,
    get_HeavyJob_diaries,
    get_HeavyJob_employees,
    get_HeavyJob_equipment_types,
    get_HeavyJob_equipment,
    get_HeavyJob_equipmenthours,
    get_HeavyJob_employeehours,
    get_Safety_incidents,
    get_Safety_incidentsV2,
    get_Safety_meetings,
    get_Setups_accounting_templates,
    get_Setups_business_units,
    get_Setups_jobs,
    get_Setups_equipment,
    get_Setups_employees,
    get_Skills_skills,
    get_Skills_employeeskills,
    get_Telematics_equipment,
    get_token,
    get_Users_business_units,
    get_Users_jobs,
    get_Users_roles,
    get_Users_subscription_groups,
    get_Users_users,
)

def parse_args():
    parser = argparse.ArgumentParser(description="Run specific API endpoint functions.")
    parser.add_argument('--function', type=str, help='Name of the function to run', required=True)
    parser.add_argument('--file_type', type=str, default="xlsx", help='File type for saving data')
    parser.add_argument('--email', type=str, default=os.getenv("TARGET_EMAIL"), help='Recipient email address')
    parser.add_argument('--rate_limit', type=float, default=0.8, help='Rate limit percentage')
    
    return parser.parse_args()

async def main():
    args = parse_args()
    logger = setup_logger()

    # Fetch environment variables and arguments
    file_type = args.file_type
    recipient_email = args.email
    rate_limit_percentage = args.rate_limit

    # Get the function to run from the arguments
    function_to_run = getattr(globals(), args.function, None)
    
    if function_to_run is None:
        print(f"Function '{args.function}' not found.")
        return

    rate_limiter = RateLimiter(rate_limit_percentage)
    
    try:
        log_process_start(logger, "Data Fetching")

        # Run the specified function
        data = function_to_run(file_type)
        filename = save_data(data, args.function, file_type)
        
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
