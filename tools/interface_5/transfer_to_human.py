import json
from typing import Any, Dict

class TransferToHuman:
    @staticmethod
    def invoke(data: Dict[str, Any], reason: str, context: Dict[str, Any],
               escalation_level: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        transfers = data.get("human_transfers", {})
        
        # Validate escalation_level
        valid_levels = ["management", "technical", "executive", "vendor"]
        if escalation_level not in valid_levels:
            return json.dumps({"error": f"Invalid escalation_level. Must be one of {valid_levels}", "halt": True})
        
        transfer_id = generate_id(transfers)
        timestamp = "2025-10-01T00:00:00"
        
        new_transfer = {
            "transfer_id": transfer_id,
            "reason": reason,
            "context": context,
            "escalation_level": escalation_level,
            "created_at": timestamp
        }
        
        transfers[transfer_id] = new_transfer
        return json.dumps({"transfer_id": transfer_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_to_human",
                "description": "Transfer the conversation to a human agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {"type": "string", "description": "Reason for transfer"},
                        "context": {"type": "object", "description": "Context information for the transfer"},
                        "escalation_level": {"type": "string", "description": "Level of escalation needed (management, technical, executive, vendor)"}
                    },
                    "required": ["reason", "context", "escalation_level"]
                }
            }
        }
