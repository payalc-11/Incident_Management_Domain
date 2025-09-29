import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class RecordWorkaround(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, implemented_by_user: str,
               effectiveness_level: str, implemented_at: str,
               status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        workarounds = data.get("workarounds", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if str(implemented_by_user) not in users:
            return json.dumps({"error": f"User {implemented_by_user} not found", "halt": True})
        
        # Validate effectiveness_level
        valid_levels = ["full_mitigation", "partial_mitigation", "minimal_impact"]
        if effectiveness_level not in valid_levels:
            return json.dumps({"error": f"Invalid effectiveness_level. Must be one of {valid_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "replaced"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        workaround_id = generate_id(workarounds)
        timestamp = "2025-10-01T00:00:00"
        
        new_workaround = {
            "workaround_id": workaround_id,
            "incident_id": incident_id,
            "implemented_by_user": implemented_by_user,
            "effectiveness_level": effectiveness_level,
            "status": status,
            "implemented_at": implemented_at,
            "created_at": timestamp
        }
        
        workarounds[workaround_id] = new_workaround
        return json.dumps({"workaround_id": workaround_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_workaround",
                "description": "Record a workaround for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "implemented_by_user": {"type": "string", "description": "User implementing workaround"},
                        "effectiveness_level": {"type": "string", "description": "Effectiveness level (full_mitigation, partial_mitigation, minimal_impact)"},
                        "implemented_at": {"type": "string", "description": "When workaround was implemented"},
                        "status": {"type": "string", "description": "Workaround status (active, inactive, replaced), defaults to active"}
                    },
                    "required": ["incident_id", "implemented_by_user", "effectiveness_level", "implemented_at"]
                }
            }
        }
