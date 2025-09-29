import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddWorkorder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, work_type: str, created_by_user: str,
               incident_id: Optional[str] = None, change_id: Optional[str] = None,
               problem_id: Optional[str] = None, assigned_to_user: Optional[str] = None,
               status: Optional[str] = 'created') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        work_orders = data.get("work_orders", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        change_requests = data.get("change_requests", {})
        problem_tickets = data.get("problem_tickets", {})
        
        # Validate user exists
        if created_by_user not in users:
            return json.dumps({"error": f"User {created_by_user} not found", "halt": True})
        
        # Validate assigned user if provided
        if assigned_to_user and assigned_to_user not in users:
            return json.dumps({"error": f"Assigned user {assigned_to_user} not found", "halt": True})
        
        # Validate related entities if provided
        if incident_id and incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if change_id and change_id not in change_requests:
            return json.dumps({"error": f"Change request {change_id} not found", "halt": True})
        if problem_id and problem_id not in problem_tickets:
            return json.dumps({"error": f"Problem ticket {problem_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ["created", "assigned", "in_progress", "completed", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        workorder_id = str(generate_id(work_orders))
        timestamp = "2025-10-01T00:00:00"
        
        new_workorder = {
            "workorder_id": workorder_id,
            "incident_id": incident_id,
            "change_id": change_id,
            "problem_id": problem_id,
            "title": title,
            "work_type": work_type,
            "status": status,
            "assigned_to_user": assigned_to_user,
            "created_by_user": created_by_user,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        work_orders[workorder_id] = new_workorder
        return json.dumps({"workorder_id": workorder_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_workorder",
                "description": "Create a new work order",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Work order title"},
                        "work_type": {"type": "string", "description": "Type of work"},
                        "created_by_user": {"type": "string", "description": "User creating the work order"},
                        "incident_id": {"type": "string", "description": "Related incident ID"},
                        "change_id": {"type": "string", "description": "Related change request ID"},
                        "problem_id": {"type": "string", "description": "Related problem ticket ID"},
                        "assigned_to_user": {"type": "string", "description": "Assigned user ID"},
                        "status": {"type": "string", "description": "Work order status (created/assigned/in_progress/completed/cancelled)"}
                    },
                    "required": ["title", "work_type", "created_by_user"]
                }
            }
        }
