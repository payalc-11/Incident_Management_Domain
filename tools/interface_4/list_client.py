import json
from typing import Any, Dict, Optional

class ListClient:
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: Optional[str] = None,
               client_name: Optional[str] = None, registration_number: Optional[str] = None,
               contact_email: Optional[str] = None, client_type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        clients = data.get("clients", {})
        results = []
        
        for client in clients.values():
            if client_id and str(client.get("client_id")) != str(client_id):
                continue
            if client_name and client_name.lower() not in client.get("client_name", "").lower():
                continue
            if registration_number and client.get("registration_number") != registration_number:
                continue
            if contact_email and client.get("contact_email", "").lower() != contact_email.lower():
                continue
            if client_type and client.get("client_type") != client_type:
                continue
            if status and client.get("status") != status:
                continue
            results.append(client)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_client",
                "description": "Discover clients with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string", "description": "Filter by client ID"},
                        "client_name": {"type": "string", "description": "Filter by client name (partial match)"},
                        "registration_number": {"type": "string", "description": "Filter by registration number"},
                        "contact_email": {"type": "string", "description": "Filter by contact email"},
                        "client_type": {"type": "string", "description": "Filter by client type (enterprise, mid_market, small_business, startup)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"}
                    },
                    "required": []
                }
            }
        }
