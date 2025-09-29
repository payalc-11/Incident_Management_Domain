import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticket_id: str, change_set: Dict[str, Any],
               status: Optional[str] = None) -> str:
        
        problem_tickets = data.get("problem_tickets", {})
        
        # Validate ticket exists
        if ticket_id not in problem_tickets:
            return json.dumps({"error": f"Ticket {ticket_id} not found", "halt": True})
        
        # Update change_set with optional parameter if provided
        if status:
            change_set["status"] = status
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            problem_tickets[ticket_id][key] = value
        
        problem_tickets[ticket_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(problem_tickets[ticket_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_ticket",
                "description": "Update a problem ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "ID of the ticket to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "status": {"type": "string", "description": "New status (open/investigating/in_progress/resolved/closed)"}
                    },
                    "required": ["ticket_id", "change_set"]
                }
            }
        }
