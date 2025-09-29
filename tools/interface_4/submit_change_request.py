import json
from typing import Any, Dict, Optional

class SubmitChangeRequest:
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, change_type: str, risk_level: str,
               requesting_user: str, incident_id: Optional[str] = None, 
               status: Optional[str] = 'requested', approved_by_user: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        change_requests = data.get("change_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        
        # Validate requesting user exists
        if str(requesting_user) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user} not found", "halt": True})
        
        # Validate approved_by user if provided
        if approved_by_user and str(approved_by_user) not in users:
            return json.dumps({"error": f"Approving user {approved_by_user} not found", "halt": True})
        
        # Validate incident if provided
        if incident_id and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate change_type
        valid_change_types = ["normal", "standard", "upgrade", "emergency"]
        if change_type not in valid_change_types:
            return json.dumps({"error": f"Invalid change_type. Must be one of {valid_change_types}", "halt": True})
        
        # Validate risk_level
        valid_risk_levels = ["low", "medium", "high"]
        if risk_level not in valid_risk_levels:
            return json.dumps({"error": f"Invalid risk_level. Must be one of {valid_risk_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["requested", "in_progress", "scheduled", "rolled_back", "completed", "failed", "approved"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        change_id = generate_id(change_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_change_request = {
            "change_id": change_id,
            "incident_id": incident_id,
            "title": title,
            "change_type": change_type,
            "risk_level": risk_level,
            "status": status,
            "requesting_user": requesting_user,
            "approved_by_user": approved_by_user,
            "scheduled_start_time": None,
            "scheduled_end_time": None,
            "actual_start_time": None,
            "actual_end_time": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        change_requests[change_id] = new_change_request
        return json.dumps({"change_id": change_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_change_request",
                "description": "Submit a new change request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Change request title"},
                        "change_type": {"type": "string", "description": "Type of change (normal, standard, upgrade, emergency)"},
                        "risk_level": {"type": "string", "description": "Risk level of the change (low, medium, high)"},
                        "requesting_user": {"type": "string", "description": "User requesting the change"},
                        "incident_id": {"type": "string", "description": "Related incident ID if applicable"},
                        "status": {"type": "string", "description": "Change request status (requested, in_progress, scheduled, rolled_back, completed, failed, approved), defaults to 'requested'"},
                        "approved_by_user": {"type": "string", "description": "User who approved the change"}
                    },
                    "required": ["title", "change_type", "risk_level", "requesting_user"]
                }
            }
        }
