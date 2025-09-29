import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateClient(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str, change_set: Dict[str, Any],
               registration_number: Optional[str] = None, contact_email: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        clients = data.get("clients", {})
        
        # Validate client exists
        if client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if registration_number:
            change_set["registration_number"] = registration_number
        if contact_email:
            change_set["contact_email"] = contact_email
        if status:
            change_set["status"] = status
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["active", "inactive", "suspended"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check unique constraints
        if "registration_number" in change_set:
            for cid, client in clients.items():
                if cid != client_id and client.get("registration_number") == change_set["registration_number"]:
                    return json.dumps({"error": f"Registration number {change_set['registration_number']} already exists", "halt": True})
        
        if "contact_email" in change_set:
            for cid, client in clients.items():
                if cid != client_id and client.get("contact_email") == change_set["contact_email"]:
                    return json.dumps({"error": f"Contact email {change_set['contact_email']} already exists", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            clients[client_id][key] = value
        
        clients[client_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(clients[client_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_client",
                "description": "Update an existing client's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string", "description": "ID of the client to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "registration_number": {"type": "string", "description": "New unique registration number if being updated"},
                        "contact_email": {"type": "string", "description": "New unique contact email if being updated"},
                        "status": {"type": "string", "description": "New status (active/inactive/suspended)"}
                    },
                    "required": ["client_id", "change_set"]
                }
            }
        }
