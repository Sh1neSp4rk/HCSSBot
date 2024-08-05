# EndpointCalls/__init__.py

"""
This package contains modules for interacting with various HCSS APIs.
Each module is responsible for fetching and processing data from specific endpoints.
"""

from .equipment360_get import (
    get_EquipmentE360_business_units,
    get_EquipmentE360_fuel_costs,
    get_EquipmentE360_work_order_costs,
    get_EquipmentE360_work_order_details,
    get_EquipmentE360_custom_fields,
    get_EquipmentE360_custom_field_categories,
)
from .heavybidestimates_get import (
    get_HeavyBidEstimates_business_units,
    get_HeavyBidEstimates_partitions,
)
from .heavyjob_get import (
    get_HeavyJob_business_units,
    get_HeavyJob_jobs,
    get_HeavyJob_jobcosts,
    get_HeavyJob_costcodes,
    get_HeavyJob_jobemployees,
    get_HeavyJob_jobequipment,
    get_HeavyJob_jobmaterials,
    get_HeavyJob_materials,
    get_HeavyJob_timecards,
    get_HeavyJob_diaries,
    get_HeavyJob_employees,
    get_HeavyJob_equipment_types,
    get_HeavyJob_equipment,
    get_HeavyJob_equipmenthours,
    get_HeavyJob_employeehours,
)
from .safety_get import (
    get_Safety_incidents,
    get_Safety_meetings,
)
from .setups_get import (
    get_Setups_accounting_templates,
    get_Setups_business_units,
    get_Setups_jobs,
    get_Setups_equipment,
    get_Setups_employees,
)
from .skills_get import (
    get_Skills_skills,
    get_Skills_employeeskills,
)
from .telematics_get import get_Telematics_equipment
from .token_get import get_token
from .users_get import (
    get_Users_business_units,
    get_Users_jobs,
    get_Users_roles,
    get_Users_subscription_groups,
    get_Users_users,
)

__all__ = [
    # Equipment E360
    "get_EquipmentE360_business_units",
    "get_EquipmentE360_fuel_costs",
    "get_EquipmentE360_work_order_costs",
    "get_EquipmentE360_work_order_details",
    "get_EquipmentE360_custom_fields",
    "get_EquipmentE360_custom_field_categories",
    
    # HeavyBid Estimates
    "get_HeavyBidEstimates_business_units",
    "get_HeavyBidEstimates_partitions",
    
    # HeavyJob
    "get_HeavyJob_business_units",
    "get_HeavyJob_jobs",
    "get_HeavyJob_jobcosts",
    "get_HeavyJob_costcodes",
    "get_HeavyJob_jobemployees",
    "get_HeavyJob_jobequipment",
    "get_HeavyJob_jobmaterials",
    "get_HeavyJob_materials",
    "get_HeavyJob_timecards",
    "get_HeavyJob_diaries",
    "get_HeavyJob_employees",
    "get_HeavyJob_equipment_types",
    "get_HeavyJob_equipment",
    "get_HeavyJob_equipmenthours",
    "get_HeavyJob_employeehours",
    
    # Safety
    "get_Safety_incidents",
    "get_Safety_meetings",
    
    # Setups
    "get_Setups_accounting_templates",
    "get_Setups_business_units",
    "get_Setups_jobs",
    "get_Setups_equipment",
    "get_Setups_employees",
    
    # Skills
    "get_Skills_skills",
    "get_Skills_employeeskills",
    
    # Telematics
    "get_Telematics_equipment",
    
    # Token
    "get_token",

    # Users
    "get_Users_business_units",
    "get_Users_jobs",
    "get_Users_roles",
    "get_Users_subscription_groups",
    "get_Users_users",
]
