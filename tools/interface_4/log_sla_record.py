import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class LogSlaRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, response_time_minutes: int,
               resolution_time_hours: int, availability_percentage: Optional[float] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        slas = data.get("service_level_agreements", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if subscription_id not in subscriptions:
            return json.dumps({"error": f"Subscription {subscription_id} not found", "halt": True})
        
        sla_id = str(generate_id(slas))
        timestamp = "2025-10-01T00:00:00"
        
        new_sla = {
            "sla_id": sla_id,
            "subscription_id": subscription_id,
            "severity_level": None,
            "response_time_minutes": response_time_minutes,
            "resolution_time_hours": resolution_time_hours,
            "availability_percentage": availability_percentage,
            "created_at": timestamp
        }
        
        slas[sla_id] = new_sla
        return json.dumps({"sla_id": sla_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_sla_record",
                "description": "Create an SLA record for a subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription"},
                        "response_time_minutes": {"type": "integer", "description": "Response time in minutes"},
                        "resolution_time_hours": {"type": "integer", "description": "Resolution time in hours"},
                        "availability_percentage": {"type": "number", "description": "Availability percentage target"}
                    },
                    "required": ["subscription_id", "response_time_minutes", "resolution_time_hours"]
                }
            }
        }
