import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateEscalation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, escalated_by_user: str,
               escalated_to_user: str, escalation_level: str, escalated_at: str,
               reason: Optional[str] = None, status: Optional[str] = 'active',
               resolved_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        escalations = data.get("incident_escalations", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate users exist
        if escalated_by_user not in users:
            return json.dumps({"error": f"User {escalated_by_user} not found", "halt": True})
        if escalated_to_user not in users:
            return json.dumps({"error": f"User {escalated_to_user} not found", "halt": True})
        
        # Validate escalation_level
        valid_levels = ["management", "technical", "executive", "vendor"]
        if escalation_level not in valid_levels:
            return json.dumps({"error": f"Invalid escalation_level. Must be one of {valid_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "resolved", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        escalation_id = str(generate_id(escalations))
        timestamp = "2025-10-01T00:00:00"
        
        new_escalation = {
            "escalation_id": escalation_id,
            "incident_id": incident_id,
            "escalated_by_user": escalated_by_user,
            "escalated_to_user": escalated_to_user,
            "escalation_level": escalation_level,
            "reason": reason,
            "status": status,
            "escalated_at": escalated_at,
            "resolved_at": resolved_at,
            "created_at": timestamp
        }
        
        escalations[escalation_id] = new_escalation
        return json.dumps({"escalation_id": escalation_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_escalation",
                "description": "Submit an escalation for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident to escalate"},
                        "escalated_by_user": {"type": "string", "description": "User initiating escalation"},
                        "escalated_to_user": {"type": "string", "description": "Target user for escalation"},
                        "escalation_level": {"type": "string", "description": "Level of escalation (management/technical/executive/vendor)"},
                        "escalated_at": {"type": "string", "description": "Timestamp of escalation"},
                        "reason": {"type": "string", "description": "Reason for escalation"},
                        "status": {"type": "string", "description": "Escalation status (active/resolved/cancelled)"},
                        "resolved_at": {"type": "string", "description": "When escalation was resolved"}
                    },
                    "required": ["incident_id", "escalated_by_user", "escalated_to_user", "escalation_level", "escalated_at"]
                }
            }
        }
