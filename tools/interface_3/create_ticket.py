import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, title: str,
               issued_by_user: str, status: Optional[str] = 'open') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        problem_tickets = data.get("problem_tickets", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if issued_by_user not in users:
            return json.dumps({"error": f"User {issued_by_user} not found", "halt": True})
        
        # Validate status
        valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        problem_id = str(generate_id(problem_tickets))
        timestamp = "2025-10-01T00:00:00"
        
        new_ticket = {
            "problem_id": problem_id,
            "incident_id": incident_id,
            "title": title,
            "status": status,
            "issued_by_user": issued_by_user,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        problem_tickets[problem_id] = new_ticket
        return json.dumps({"ticket_id": problem_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_ticket",
                "description": "Create a problem ticket for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Parent incident ID"},
                        "title": {"type": "string", "description": "Problem ticket title"},
                        "issued_by_user": {"type": "string", "description": "User creating the ticket"},
                        "status": {"type": "string", "description": "Ticket status (open/investigating/in_progress/resolved/closed)"}
                    },
                    "required": ["incident_id", "title", "issued_by_user"]
                }
            }
        }
