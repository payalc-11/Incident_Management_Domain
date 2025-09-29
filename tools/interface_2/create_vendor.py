import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateVendor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_name: str, vendor_email: str,
               vendor_phone: str, vendor_type: str, status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        vendors = data.get("vendors", {})
        
        # Validate vendor_type
        valid_vendor_types = ["technology_provider", "infrastructure_provider", "security_provider",
                             "consulting_services", "maintenance_services", "cloud_provider", "payment_processor"]
        if vendor_type not in valid_vendor_types:
            return json.dumps({"error": f"Invalid vendor_type. Must be one of {valid_vendor_types}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique vendor_name
        for vendor in vendors.values():
            if vendor.get("vendor_name") == vendor_name:
                return json.dumps({"error": f"Vendor name {vendor_name} already exists", "halt": True})
        
        # Check for unique contact_email
        for vendor in vendors.values():
            if vendor.get("contact_email") == vendor_email:
                return json.dumps({"error": f"Contact email {vendor_email} already exists", "halt": True})
        
        # Check for unique contact_phone
        for vendor in vendors.values():
            if vendor.get("contact_phone") == vendor_phone:
                return json.dumps({"error": f"Contact phone {vendor_phone} already exists", "halt": True})
        
        vendor_id = str(generate_id(vendors))
        timestamp = "2025-10-01T00:00:00"
        
        new_vendor = {
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "vendor_type": vendor_type,
            "contact_email": vendor_email,
            "contact_phone": vendor_phone,
            "status": status,
            "created_at": timestamp
        }
        
        vendors[vendor_id] = new_vendor
        return json.dumps({"vendor_id": vendor_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_vendor",
                "description": "Create a new vendor in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_name": {"type": "string", "description": "Unique name of the vendor"},
                        "vendor_email": {"type": "string", "description": "Unique email address"},
                        "vendor_phone": {"type": "string", "description": "Unique phone number"},
                        "vendor_type": {"type": "string", "description": "Type of vendor (technology_provider/infrastructure_provider/security_provider/consulting_services/maintenance_services/cloud_provider/payment_processor)"},
                        "status": {"type": "string", "description": "Vendor status (active/inactive/suspended)"}
                    },
                    "required": ["vendor_name", "vendor_email", "vendor_phone", "vendor_type"]
                }
            }
        }
