import json
from typing import Any, Dict, Optional

class DiscoverIncident:
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               client_id: Optional[str] = None, severity: Optional[str] = None,
               status: Optional[str] = None, assigned_to_user_id: Optional[str] = None,
               reporter_user_id: Optional[str] = None) -> str:
        
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if incident_id and str(incident.get("incident_id")) != str(incident_id):
                continue
            if client_id and incident.get("client_id") != client_id:
                continue
            if severity and incident.get("severity") != severity:
                continue
            if status and incident.get("status") != status:
                continue
            if assigned_to_user_id and incident.get("assigned_to_user_id") != assigned_to_user_id:
                continue
            if reporter_user_id and incident.get("reporter_user_id") != reporter_user_id:
                continue
            results.append(incident)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_incident",
                "description": "Discover incidents with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "client_id": {"type": "string", "description": "Filter by client"},
                        "severity": {"type": "string", "description": "Filter by severity (P1, P2, P3, P4)"},
                        "status": {"type": "string", "description": "Filter by status (open, investigating, in_progress, resolved, closed)"},
                        "assigned_to_user_id": {"type": "string", "description": "Filter by assignee"},
                        "reporter_user_id": {"type": "string", "description": "Filter by reporter"}
                    },
                    "required": []
                }
            }
        }
