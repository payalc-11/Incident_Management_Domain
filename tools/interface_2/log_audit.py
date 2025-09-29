import json
from typing import Any, Dict

class LogAudit:
    @staticmethod
    def invoke(data: Dict[str, Any], action_type: str, entity_type: str,
               entity_id: str, performed_by_user: str, action_details: Dict[str, Any],
               timestamp: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        audit_logs = data.get("audit_logs", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(performed_by_user) not in users:
            return json.dumps({"error": f"User {performed_by_user} not found", "halt": True})
        
        audit_id = generate_id(audit_logs)
        
        new_audit = {
            "audit_id": audit_id,
            "action": action_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "audit_by_user": performed_by_user,
            "created_at": timestamp
        }
        
        # Store action details separately if needed
        audit_logs[audit_id] = new_audit
        
        return json.dumps({"audit_id": audit_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit",
                "description": "Log an audit entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_type": {"type": "string", "description": "Type of action being audited"},
                        "entity_type": {"type": "string", "description": "Type of entity affected"},
                        "entity_id": {"type": "string", "description": "ID of the entity"},
                        "performed_by_user": {"type": "string", "description": "User performing the action"},
                        "action_details": {"type": "object", "description": "Details of the action"},
                        "timestamp": {"type": "string", "description": "When action was performed (YYYY-MM-DD)"}
                    },
                    "required": ["action_type", "entity_type", "entity_id", "performed_by_user", "action_details", "timestamp"]
                }
            }
        }
