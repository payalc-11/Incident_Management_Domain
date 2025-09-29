import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, email: str, role: str,
               department: Optional[str] = None, client_id: Optional[str] = None,
               vendor_id: Optional[str] = None, timezone: Optional[str] = 'UTC',
               status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        clients = data.get("clients", {})
        vendors = data.get("vendors", {})
        
        # Validate role
        valid_roles = ["system_administrator", "incident_manager", "technical_support", 
                      "account_manager", "executive", "client_contact", "vendor_contact"]
        if role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "on_leave"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique email
        for user in users.values():
            if user.get("email") == email:
                return json.dumps({"error": f"Email {email} already exists", "halt": True})
        
        # Validate client_id if provided
        if client_id and client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        
        # Validate vendor_id if provided
        if vendor_id and vendor_id not in vendors:
            return json.dumps({"error": f"Vendor {vendor_id} not found", "halt": True})
        
        user_id = str(generate_id(users))
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "department": department,
            "client_id": client_id,
            "vendor_id": vendor_id,
            "timezone": timezone,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Register a new user in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the user"},
                        "email": {"type": "string", "description": "Unique email address"},
                        "role": {"type": "string", "description": "User role (system_administrator/incident_manager/technical_support/account_manager/executive/client_contact/vendor_contact)"},
                        "department": {"type": "string", "description": "Department of the user"},
                        "client_id": {"type": "string", "description": "Associated client ID"},
                        "vendor_id": {"type": "string", "description": "Associated vendor ID"},
                        "timezone": {"type": "string", "description": "User timezone (defaults to UTC)"},
                        "status": {"type": "string", "description": "User status (active/inactive/on_leave)"}
                    },
                    "required": ["name", "email", "role"]
                }
            }
        }
