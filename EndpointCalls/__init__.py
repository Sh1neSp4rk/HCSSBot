# EndpointCalls/__init__.py

"""
This package contains modules for interacting with various HCSS APIs.
Each module is responsible for fetching and processing data from specific endpoints.
"""

from .equipmentE360_get import (
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
    get_heavyjob_businessunits,
    get_heavyjob_jobs,
    get_heavyjob_jobcosts,
    get_heavyjob_costcodes,
    get_heavyjob_jobemployees,
    get_heavyjob_jobequipment,
    get_heavyjob_jobmaterials,
    get_heavyjob_materials,
    get_heavyjob_timecards,
    get_heavyjob_user,
    get_heavyjob_diaries,
    get_heavyjob_employees,
    get_heavyjob_equipment_types,
    get_heavyjob_equipment,
    get_heavyjob_equipmenthours,
    get_heavyjob_employeehours,
)
from .safety_get import get_Safety_data
from .setups_get import (
    get_Setups_accounting_templates,
    get_Setups_business_units,
    get_Setups_jobs,
    get_Setups_equipment,
    get_Setups_employees,
)
from .skills_get import (
    fetch_Skills_skills,
    fetch_Skills_employee_skills,
    get_Skills_all_skills,
    get_Skills_all_employee_skills,
)
from .telematics_get import get_Telematics_equipment
from .token_get import get_token

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
    "get_heavyjob_businessunits",
    "get_heavyjob_jobs",
    "get_heavyjob_jobcosts",
    "get_heavyjob_costcodes",
    "get_heavyjob_jobemployees",
    "get_heavyjob_jobequipment",
    "get_heavyjob_jobmaterials",
    "get_heavyjob_materials",
    "get_heavyjob_timecards",
    "get_heavyjob_user",
    "get_heavyjob_diaries",
    "get_heavyjob_employees",
    "get_heavyjob_equipment_types",
    "get_heavyjob_equipment",
    "get_heavyjob_equipmenthours",
    "get_heavyjob_employeehours",
    
    # Safety
    "get_Safety_data",
    
    # Setups
    "get_Setups_accounting_templates",
    "get_Setups_business_units",
    "get_Setups_jobs",
    "get_Setups_equipment",
    "get_Setups_employees",
    
    # Skills
    "fetch_Skills_skills",
    "fetch_Skills_employee_skills",
    "get_Skills_all_skills",
    "get_Skills_all_employee_skills",
    
    # Telematics
    "get_Telematics_equipment",
    
    # Token
    "get_token",
]
