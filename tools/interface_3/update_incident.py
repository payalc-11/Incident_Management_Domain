import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, change_set: Dict[str, Any],
               status: Optional[str] = None, assigned_to_user_id: Optional[str] = None,
               resolution_timestamp: Optional[str] = None) -> str:
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if status:
            change_set["status"] = status
        if assigned_to_user_id:
            change_set["assigned_to_user_id"] = assigned_to_user_id
        if resolution_timestamp:
            change_set["resolution_timestamp"] = resolution_timestamp
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate assigned user if being updated
        if "assigned_to_user_id" in change_set and change_set["assigned_to_user_id"]:
            if change_set["assigned_to_user_id"] not in users:
                return json.dumps({"error": f"Assigned user {change_set['assigned_to_user_id']} not found", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            incidents[incident_id][key] = value
        
        incidents[incident_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(incidents[incident_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_incident",
                "description": "Update an existing incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "status": {"type": "string", "description": "New status (open/investigating/in_progress/resolved/closed)"},
                        "assigned_to_user_id": {"type": "string", "description": "New assignee"},
                        "resolution_timestamp": {"type": "string", "description": "Resolution timestamp"}
                    },
                    "required": ["incident_id", "change_set"]
                }
            }
        }
