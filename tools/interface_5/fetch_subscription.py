import json
from typing import Any, Dict, Optional

class FetchSubscription:
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: Optional[str] = None,
               client_id: Optional[str] = None, product_id: Optional[str] = None,
               sla_tier: Optional[str] = None, status: Optional[str] = None) -> str:
        
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if subscription_id and str(subscription.get("subscription_id")) != str(subscription_id):
                continue
            if client_id and subscription.get("client_id") != client_id:
                continue
            if product_id and subscription.get("product_id") != product_id:
                continue
            if sla_tier and subscription.get("sla_tier") != sla_tier:
                continue
            if status and subscription.get("status") != status:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_subscription",
                "description": "Discover subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "client_id": {"type": "string", "description": "Filter by client"},
                        "product_id": {"type": "string", "description": "Filter by product"},
                        "sla_tier": {"type": "string", "description": "Filter by SLA tier (basic, standard, premium)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, cancelled, expired)"}
                    },
                    "required": []
                }
            }
        }
