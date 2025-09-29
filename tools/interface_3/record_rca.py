import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class RecordRca(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, conducted_by_user: str,
               analysis_method: str, status: Optional[str] = 'in_progress',
               completed_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        root_cause_analysis = data.get("root_cause_analysis", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if str(conducted_by_user) not in users:
            return json.dumps({"error": f"User {conducted_by_user} not found", "halt": True})
        
        # Validate analysis_method
        valid_methods = ["five_whys", "fishbone_diagram", "fault_tree_analysis", "timeline_analysis"]
        if analysis_method not in valid_methods:
            return json.dumps({"error": f"Invalid analysis_method. Must be one of {valid_methods}", "halt": True})
        
        # Validate status
        valid_statuses = ["in_progress", "completed", "reviewed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        analysis_id = generate_id(root_cause_analysis)
        timestamp = "2025-10-01T00:00:00"
        
        new_analysis = {
            "analysis_id": analysis_id,
            "incident_id": incident_id,
            "conducted_by_user": conducted_by_user,
            "analysis_method": analysis_method,
            "status": status,
            "completed_at": completed_at,
            "created_at": timestamp
        }
        
        root_cause_analysis[analysis_id] = new_analysis
        return json.dumps({"analysis_id": analysis_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_rca",
                "description": "Conduct root cause analysis for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "conducted_by_user": {"type": "string", "description": "User conducting RCA"},
                        "analysis_method": {"type": "string", "description": "Method of analysis (five_whys, fishbone_diagram, fault_tree_analysis, timeline_analysis)"},
                        "status": {"type": "string", "description": "RCA status (in_progress, completed, reviewed), defaults to in_progress"},
                        "completed_at": {"type": "string", "description": "When RCA was completed"}
                    },
                    "required": ["incident_id", "conducted_by_user", "analysis_method"]
                }
            }
        }
