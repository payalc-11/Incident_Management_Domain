import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class LogIncidentUpdate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, update_type: str,
               update_details: Dict[str, Any], updated_by_user: str,
               update_timestamp: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incident_updates = data.get("incident_updates", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if updated_by_user not in users:
            return json.dumps({"error": f"User {updated_by_user} not found", "halt": True})
        
        update_id = str(generate_id(incident_updates))
        
        # Extract field changes from update_details
        field_changed = update_details.get("field_changed", "multiple_fields")
        old_value = update_details.get("old_value", "")
        new_value = update_details.get("new_value", "")
        
        new_update = {
            "update_id": update_id,
            "incident_id": incident_id,
            "updated_by_user": updated_by_user,
            "update_type": update_type,
            "field_changed": field_changed,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": update_timestamp
        }
        
        incident_updates[update_id] = new_update
        return json.dumps({"update_id": update_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_incident_update",
                "description": "Log an update to an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "update_type": {"type": "string", "description": "Type of update"},
                        "update_details": {"type": "object", "description": "Details of the update"},
                        "updated_by_user": {"type": "string", "description": "User making the update"},
                        "update_timestamp": {"type": "string", "description": "When update was made"}
                    },
                    "required": ["incident_id", "update_type", "update_details", "updated_by_user", "update_timestamp"]
                }
            }
        }
