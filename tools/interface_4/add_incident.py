import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, category: str, severity: str,
               impact_level: str, urgency_level: str, client_id: str,
               component_id: str, reporter_user_id: str, detection_timestamp: str,
               status: Optional[str] = 'open', assigned_to_user_id: Optional[str] = None,
               resolution_timestamp: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        clients = data.get("clients", {})
        components = data.get("infrastructure_components", {})
        users = data.get("users", {})
        
        # Validate severity
        valid_severities = ["P1", "P2", "P3", "P4"]
        if severity not in valid_severities:
            return json.dumps({"error": f"Invalid severity. Must be one of {valid_severities}", "halt": True})
        
        # Validate levels
        valid_levels = ["low", "medium", "high", "critical"]
        if impact_level not in valid_levels:
            return json.dumps({"error": f"Invalid impact_level. Must be one of {valid_levels}", "halt": True})
        if urgency_level not in valid_levels:
            return json.dumps({"error": f"Invalid urgency_level. Must be one of {valid_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate entities exist
        if client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        if component_id not in components:
            return json.dumps({"error": f"Component {component_id} not found", "halt": True})
        if reporter_user_id not in users:
            return json.dumps({"error": f"Reporter user {reporter_user_id} not found", "halt": True})
        if assigned_to_user_id and assigned_to_user_id not in users:
            return json.dumps({"error": f"Assigned user {assigned_to_user_id} not found", "halt": True})
        
        incident_id = str(generate_id(incidents))
        timestamp = "2025-10-01T00:00:00"
        
        new_incident = {
            "incident_id": incident_id,
            "title": title,
            "category": category,
            "severity": severity,
            "impact_level": impact_level,
            "urgency_level": urgency_level,
            "status": status,
            "client_id": client_id,
            "component_id": component_id,
            "reporter_user_id": reporter_user_id,
            "assigned_to_user_id": assigned_to_user_id,
            "detection_timestamp": detection_timestamp,
            "resolution_timestamp": resolution_timestamp,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        incidents[incident_id] = new_incident
        return json.dumps({"incident_id": incident_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_incident",
                "description": "Report a new incident in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Incident title"},
                        "category": {"type": "string", "description": "Incident category"},
                        "severity": {"type": "string", "description": "Severity level (P1/P2/P3/P4)"},
                        "impact_level": {"type": "string", "description": "Impact level (low/medium/high/critical)"},
                        "urgency_level": {"type": "string", "description": "Urgency level (low/medium/high/critical)"},
                        "client_id": {"type": "string", "description": "ID of affected client"},
                        "component_id": {"type": "string", "description": "ID of affected component"},
                        "reporter_user_id": {"type": "string", "description": "ID of user reporting the incident"},
                        "detection_timestamp": {"type": "string", "description": "When incident was detected"},
                        "status": {"type": "string", "description": "Incident status (open/investigating/in_progress/resolved/closed)"},
                        "assigned_to_user_id": {"type": "string", "description": "ID of assigned user"},
                        "resolution_timestamp": {"type": "string", "description": "When incident was resolved"}
                    },
                    "required": ["title", "category", "severity", "impact_level", "urgency_level", "client_id", "component_id", "reporter_user_id", "detection_timestamp"]
                }
            }
        }
