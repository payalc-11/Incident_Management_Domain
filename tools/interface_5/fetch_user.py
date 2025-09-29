import json
from typing import Any, Dict, Optional

class FetchUser:
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               email: Optional[str] = None, role: Optional[str] = None,
               client_id: Optional[str] = None, vendor_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if user_id and str(user.get("user_id")) != str(user_id):
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if role and user.get("role") != role:
                continue
            if client_id and user.get("client_id") != client_id:
                continue
            if vendor_id and user.get("vendor_id") != vendor_id:
                continue
            if status and user.get("status") != status:
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_user",
                "description": "Discover users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by email address"},
                        "role": {"type": "string", "description": "Filter by role (system_administrator, incident_manager, technical_support, account_manager, executive, client_contact, vendor_contact)"},
                        "client_id": {"type": "string", "description": "Filter by associated client"},
                        "vendor_id": {"type": "string", "description": "Filter by associated vendor"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, on_leave)"}
                    },
                    "required": []
                }
            }
        }
