import json
from typing import Any, Dict, Optional

class DiscoverVendor:
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_id: Optional[str] = None,
               vendor_name: Optional[str] = None, vendor_email: Optional[str] = None,
               vendor_phone: Optional[str] = None, vendor_type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        vendors = data.get("vendors", {})
        results = []
        
        for vendor in vendors.values():
            if vendor_id and str(vendor.get("vendor_id")) != str(vendor_id):
                continue
            if vendor_name and vendor_name.lower() not in vendor.get("vendor_name", "").lower():
                continue
            if vendor_email and vendor.get("contact_email", "").lower() != vendor_email.lower():
                continue
            if vendor_phone and vendor.get("contact_phone") != vendor_phone:
                continue
            if vendor_type and vendor.get("vendor_type") != vendor_type:
                continue
            if status and vendor.get("status") != status:
                continue
            results.append(vendor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_vendor",
                "description": "Discover vendors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "Filter by vendor ID"},
                        "vendor_name": {"type": "string", "description": "Filter by vendor name (partial match)"},
                        "vendor_email": {"type": "string", "description": "Filter by email"},
                        "vendor_phone": {"type": "string", "description": "Filter by phone"},
                        "vendor_type": {"type": "string", "description": "Filter by vendor type (technology_provider, infrastructure_provider, security_provider, consulting_services, maintenance_services, cloud_provider, payment_processor)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"}
                    },
                    "required": []
                }
            }
        }
