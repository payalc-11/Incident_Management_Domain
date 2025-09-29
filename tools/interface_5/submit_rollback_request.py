import json
from typing import Any, Dict, Optional

class SubmitRollbackRequest:
    @staticmethod
    def invoke(data: Dict[str, Any], change_id: str, requesting_user: str,
               incident_id: Optional[str] = None, status: Optional[str] = 'requested',
               approved_by_user: Optional[str] = None, completed_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        rollback_requests = data.get("rollback_requests", {})
        change_requests = data.get("change_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        
        # Validate change request exists
        if str(change_id) not in change_requests:
            return json.dumps({"error": f"Change request {change_id} not found", "halt": True})
        
        # Validate requesting user exists
        if str(requesting_user) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user} not found", "halt": True})
        
        # Validate approved_by user if provided
        if approved_by_user and str(approved_by_user) not in users:
            return json.dumps({"error": f"Approving user {approved_by_user} not found", "halt": True})
        
        # Validate incident if provided
        if incident_id and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ["requested", "in_progress", "failed", "approved"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        rollback_id = generate_id(rollback_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_rollback = {
            "rollback_id": rollback_id,
            "change_id": change_id,
            "incident_id": incident_id,
            "requesting_user": requesting_user,
            "status": status,
            "approved_by_user": approved_by_user,
            "completed_at": completed_at,
            "created_at": timestamp
        }
        
        rollback_requests[rollback_id] = new_rollback
        return json.dumps({"rollback_id": rollback_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_rollback_request",
                "description": "Create a rollback request for a change",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "change_id": {"type": "string", "description": "ID of the change to rollback"},
                        "requesting_user": {"type": "string", "description": "User requesting rollback"},
                        "incident_id": {"type": "string", "description": "Related incident ID if applicable"},
                        "status": {"type": "string", "description": "Rollback status (requested, in_progress, failed, approved), defaults to 'requested'"},
                        "approved_by_user": {"type": "string", "description": "User who approved the rollback"},
                        "completed_at": {"type": "string", "description": "When rollback was completed (YYYY-MM-DD)"}
                    },
                    "required": ["change_id", "requesting_user"]
                }
            }
        }
