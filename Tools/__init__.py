# Tools/__init__.py

"""
Tools Package

This package includes various modules for handling API requests,
rate limiting, data fetching, data saving, logging, email sending, 
and file cleanup.
"""

# Rate Limiting
from .rate_limiter import RateLimiter

# Progress Bars
from .progress_bars import (
    fetch_data_with_progress,
    fetch_paginated_data_with_progress
)

# Logging
from .logger import (
    setup_logger,
    log_process_start,
    log_process_completion,
    log_error,
    set_last_successful_date,
    get_last_successful_date_from_log
)

# Email Sending
from .email_sender import send_email

# Data Saving
from .data_saver import save_data

# File Cleanup
from .cleanup_files import cleanup_files

__all__ = [
    # Rate Limiting
    "RateLimiter",

    # Progress Bars
    "fetch_data_with_progress",
    "fetch_paginated_data_with_progress",

    # Logging
    "setup_logger",
    "log_process_start",
    "log_process_completion",
    "log_error",
    "set_last_successful_date",
    "get_last_successful_date_from_log"

    # Email Sending
    "send_email",

    # Data Saving
    "save_data",

    # File Cleanup
    "cleanup_files"
]
