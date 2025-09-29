import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, change_set: Dict[str, Any],
               role: Optional[str] = None, status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        
        # Validate user exists
        if user_id not in users:
            return json.dumps({"error": f"User {user_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if role:
            change_set["role"] = role
        if status:
            change_set["status"] = status
        
        # Validate role if being updated
        if "role" in change_set:
            valid_roles = ["system_administrator", "incident_manager", "technical_support",
                          "account_manager", "executive", "client_contact", "vendor_contact"]
            if change_set["role"] not in valid_roles:
                return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}", "halt": True})
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["active", "inactive", "on_leave"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check unique email if being updated
        if "email" in change_set:
            for uid, user in users.items():
                if uid != user_id and user.get("email") == change_set["email"]:
                    return json.dumps({"error": f"Email {change_set['email']} already exists", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            users[user_id][key] = value
        
        users[user_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(users[user_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user",
                "description": "Update an existing user's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "role": {"type": "string", "description": "New role assignment"},
                        "status": {"type": "string", "description": "New status (active/inactive/on_leave)"}
                    },
                    "required": ["user_id", "change_set"]
                }
            }
        }
