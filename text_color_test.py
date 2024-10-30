import logging
from utils_logging import setup_logging, logger  # Import the setup_logging function and logger

# Set up logging to output to app.log
log_file = 'logs/app.log'
setup_logging(log_file)

# Access the console handler from the logger
console_handler = logger.handlers[1]  # Assuming the console handler is the second one added

# Temporarily set the console handler level to DEBUG for this script
console_handler.setLevel(logging.DEBUG)

# Define standard colors
standard_colors = {
    "Black": "\033[30m",
    "Red": "\033[31m",
    "Green": "\033[32m",
    "Yellow": "\033[33m",
    "Blue": "\033[34m",
    "Magenta": "\033[35m",
    "Cyan": "\033[36m",
    "White": "\033[37m",
}

# Define bright colors
bright_colors = {
    "Bright Black (Gray)": "\033[90m",
    "Bright Red": "\033[91m",
    "Bright Green": "\033[92m",
    "Bright Yellow": "\033[93m",
    "Bright Blue": "\033[94m",
    "Bright Magenta": "\033[95m",
    "Bright Cyan": "\033[96m",
    "Bright White": "\033[97m",
}

# Define background colors
background_colors = {
    "Background Black": "\033[40m",
    "Background Red": "\033[41m",
    "Background Green": "\033[42m",
    "Background Yellow": "\033[43m",
    "Background Blue": "\033[44m",
    "Background Magenta": "\033[45m",
    "Background Cyan": "\033[46m",
    "Background White": "\033[47m",
}

# Define bright background colors
bright_background_colors = {
    "Bright Background Black (Gray)": "\033[100m",
    "Bright Background Red": "\033[101m",
    "Bright Background Green": "\033[102m",
    "Bright Background Yellow": "\033[103m",
    "Bright Background Blue": "\033[104m",
    "Bright Background Magenta": "\033[105m",
    "Bright Background Cyan": "\033[106m",
    "Bright Background White": "\033[107m",
}

# Function to print color groups
def print_color_group(color_group):
    for color_name, color_code in color_group.items():
        print(f"{color_code}{color_name}\033[0m")  # Reset to default after each color

# Print all color groups
print("Standard Colors:")
print_color_group(standard_colors)
logger.info("Displayed standard colors.")

print("\nBright Colors:")
print_color_group(bright_colors)
logger.info("Displayed bright colors.")

print("\nBackground Colors:")
print_color_group(background_colors)
logger.info("Displayed background colors.")

print("\nBright Background Colors:")
print_color_group(bright_background_colors)
logger.info("Displayed bright background colors.")

# Test logging at each level
print("\nLog Levels:")
logger.debug("This is a debug message for testing.")
logger.info("This is an info message for testing.")
logger.warning("This is a warning message for testing.")
logger.error("This is an error message for testing.")
logger.critical("This is a critical message for testing.")

# Restore the console handler level back to INFO
console_handler.setLevel(logging.INFO)
