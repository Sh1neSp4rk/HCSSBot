# EndpointCalls/__init__.py

"""
This package contains modules for interacting with various HCSS APIs.
Each module is responsible for fetching and processing data from specific endpoints.
"""

from .equipmentE360_get import (
    get_business_units,
    get_fuel_costs,
    get_work_order_costs,
    get_work_order_details,
    get_custom_fields,
    get_custom_field_categories,
)
from .heavybidestimates_get import (
    get_heavybidestimates_business_units,
    get_heavybidestimates_partitions,
)
from .heavyjob_get import get_heavyjob_data
from .safety_get import get_safety_data
from .setups_get import (
    get_accounting_templates,
    get_business_units,
    get_jobs,
    get_equipment,
    get_employees,
)
from .skills_get import (
    fetch_skills,
    fetch_employee_skills,
    get_all_skills,
    get_all_employee_skills,
)
from .telematics_get import get_equipment
from .token_get import get_token

__all__ = [
    # Equipment E360
    "get_business_units",
    "get_fuel_costs",
    "get_work_order_costs",
    "get_work_order_details",
    "get_custom_fields",
    "get_custom_field_categories",
    
    # HeavyBid Estimates
    "get_heavybidestimates_business_units",
    "get_heavybidestimates_partitions",
    
    # HeavyJob
    "get_heavyjob_data",
    
    # Safety
    "get_safety_data",
    
    # Setups
    "get_accounting_templates",
    "get_business_units",
    "get_jobs",
    "get_equipment",
    "get_employees",
    
    # Skills
    "fetch_skills",
    "fetch_employee_skills",
    "get_all_skills",
    "get_all_employee_skills",
    
    # Telematics
    "get_equipment",
    
    # Token
    "get_token",
]
