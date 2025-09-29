import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddClientSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str, product_id: str,
               subscription_type: str, sla_tier: str, start_date: str,
               end_date: str, rto_hours: Optional[int] = None,
               status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        subscriptions = data.get("subscriptions", {})
        clients = data.get("clients", {})
        products = data.get("products", {})
        
        # Validate client exists
        if client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        
        # Validate product exists
        if product_id not in products:
            return json.dumps({"error": f"Product {product_id} not found", "halt": True})
        
        # Validate subscription_type
        valid_subscription_types = ["trial", "limited_service", "full_service", "custom"]
        if subscription_type not in valid_subscription_types:
            return json.dumps({"error": f"Invalid subscription_type. Must be one of {valid_subscription_types}", "halt": True})
        
        # Validate sla_tier
        valid_sla_tiers = ["basic", "standard", "premium"]
        if sla_tier not in valid_sla_tiers:
            return json.dumps({"error": f"Invalid sla_tier. Must be one of {valid_sla_tiers}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "cancelled", "expired"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        subscription_id = str(generate_id(subscriptions))
        timestamp = "2025-10-01T00:00:00"
        
        new_subscription = {
            "subscription_id": subscription_id,
            "client_id": client_id,
            "product_id": product_id,
            "subscription_type": subscription_type,
            "sla_tier": sla_tier,
            "rto_hours": rto_hours,
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        subscriptions[subscription_id] = new_subscription
        return json.dumps({"subscription_id": subscription_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_client_subscription",
                "description": "Create a new subscription for a client",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string", "description": "ID of the client"},
                        "product_id": {"type": "string", "description": "ID of the product"},
                        "subscription_type": {"type": "string", "description": "Type of subscription (trial/limited_service/full_service/custom)"},
                        "sla_tier": {"type": "string", "description": "SLA tier (basic/standard/premium)"},
                        "start_date": {"type": "string", "description": "Subscription start date (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "Subscription end date (YYYY-MM-DD)"},
                        "rto_hours": {"type": "integer", "description": "Recovery time objective in hours"},
                        "status": {"type": "string", "description": "Subscription status (active/inactive/cancelled/expired)"}
                    },
                    "required": ["client_id", "product_id", "subscription_type", "sla_tier", "start_date", "end_date"]
                }
            }
        }
