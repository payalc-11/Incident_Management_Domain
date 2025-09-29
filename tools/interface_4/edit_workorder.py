import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class EditWorkorder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], workorder_id: str, change_set: Dict[str, Any],
               status: Optional[str] = None, assigned_to_user: Optional[str] = None) -> str:
        
        work_orders = data.get("work_orders", {})
        users = data.get("users", {})
        
        # Validate workorder exists
        if workorder_id not in work_orders:
            return json.dumps({"error": f"Work order {workorder_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if status:
            change_set["status"] = status
        if assigned_to_user:
            change_set["assigned_to_user"] = assigned_to_user
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["created", "assigned", "in_progress", "completed", "cancelled"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate assigned user if being updated
        if "assigned_to_user" in change_set and change_set["assigned_to_user"]:
            if change_set["assigned_to_user"] not in users:
                return json.dumps({"error": f"Assigned user {change_set['assigned_to_user']} not found", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            work_orders[workorder_id][key] = value
        
        work_orders[workorder_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(work_orders[workorder_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "edit_workorder",
                "description": "Update a work order",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "workorder_id": {"type": "string", "description": "ID of the work order to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "status": {"type": "string", "description": "New status (created/assigned/in_progress/completed/cancelled)"},
                        "assigned_to_user": {"type": "string", "description": "New assigned user"}
                    },
                    "required": ["workorder_id", "change_set"]
                }
            }
        }
