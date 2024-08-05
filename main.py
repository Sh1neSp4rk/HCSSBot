import argparse
import asyncio
import os
from Tools.logger import setup_logger, log_process_start, log_process_completion, log_error
from Tools.rate_limiter import RateLimiter
from Tools.data_saver import save_data
from Tools.cleanup_files import cleanup_files
from Tools.email_sender import send_email

# Import the FUNCTION_MAP from function_map.py
from EndpointCalls.function_map import FUNCTION_MAP

def parse_args():
    parser = argparse.ArgumentParser(description="Run specific API endpoint functions.")
    parser.add_argument('--function', type=str, help='Name of the function to run (or leave empty to run all get_ functions)')
    parser.add_argument('--filetype', type=str, default="xlsx", help='File type for saving data')
    parser.add_argument('--email', type=str, default=os.getenv("TARGET_EMAIL"), help='Recipient email address')
    parser.add_argument('--ratelimit', type=float, default=0.8, help='Rate limit percentage')
    return parser.parse_args()

async def main():
    args = parse_args()
    logger = setup_logger()

    # Fetch environment variables and arguments
    file_type = args.filetype
    recipient_email = args.email
    rate_limit_percentage = args.ratelimit

    # Get the list of functions to run
    functions_to_run = {}

    if args.function:
        # If a specific function is provided, get that one
        function_to_run = FUNCTION_MAP.get(args.function)
        if function_to_run is None:
            print(f"Function '{args.function}' not found.")
            return
        functions_to_run = {args.function: function_to_run}
    else:
        # If no function is provided, get all functions starting with 'get_'
        functions_to_run = {name: func for name, func in FUNCTION_MAP.items() if name.startswith('get_')}

    rate_limiter = RateLimiter(rate_limit_percentage)

    for func_name, function_to_run in functions_to_run.items():
        try:
            log_process_start(logger, f"Data Fetching for {func_name}")

            # Call the function without worrying about business unit IDs here
            data = function_to_run(file_type)
            
            filename = save_data(data, func_name, file_type)
            
            log_process_completion(logger, f"Data Fetching for {func_name}")
            
            log_process_start(logger, f"Sending Email for {func_name}")
            send_email([filename], recipient_email)
            log_process_completion(logger, f"Sending Email for {func_name}")

        except Exception as e:
            log_error(logger, f"An error occurred while running {func_name}: {e}")

        finally:
            cleanup_files("Files")

if __name__ == "__main__":
    asyncio.run(main())
