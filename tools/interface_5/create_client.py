import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateClient(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_name: str, registration_number: str,
               contact_email: str, client_type: str, country: Optional[str] = None,
               industry: Optional[str] = None, status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        clients = data.get("clients", {})
        
        # Validate client_type
        valid_client_types = ["enterprise", "mid_market", "small_business", "startup"]
        if client_type not in valid_client_types:
            return json.dumps({"error": f"Invalid client_type. Must be one of {valid_client_types}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique registration_number
        for client in clients.values():
            if client.get("registration_number") == registration_number:
                return json.dumps({"error": f"Registration number {registration_number} already exists", "halt": True})
        
        # Check for unique contact_email
        for client in clients.values():
            if client.get("contact_email") == contact_email:
                return json.dumps({"error": f"Contact email {contact_email} already exists", "halt": True})
        
        client_id = str(generate_id(clients))
        timestamp = "2025-10-01T00:00:00"
        
        new_client = {
            "client_id": client_id,
            "client_name": client_name,
            "registration_number": registration_number,
            "contact_email": contact_email,
            "client_type": client_type,
            "industry": industry,
            "country": country,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        clients[client_id] = new_client
        return json.dumps({"client_id": client_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_client",
                "description": "Create a new client in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_name": {"type": "string", "description": "Name of the client"},
                        "registration_number": {"type": "string", "description": "Unique registration number"},
                        "contact_email": {"type": "string", "description": "Unique contact email address"},
                        "client_type": {"type": "string", "description": "Type of client (enterprise/mid_market/small_business/startup)"},
                        "country": {"type": "string", "description": "Country of the client"},
                        "industry": {"type": "string", "description": "Industry sector of the client"},
                        "status": {"type": "string", "description": "Status of the client (active/inactive/suspended)"}
                    },
                    "required": ["client_name", "registration_number", "contact_email", "client_type"]
                }
            }
        }
