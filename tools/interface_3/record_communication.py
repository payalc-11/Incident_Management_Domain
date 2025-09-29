import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class RecordCommunication(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, sender_id: str,
               recipient_id: str, communication_type: str, delivery_method: str,
               delivery_status: Optional[str] = 'pending', 
               recipient_type: Optional[str] = None,
               sent_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        communications = data.get("communications", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate sender exists
        if str(sender_id) not in users:
            return json.dumps({"error": f"Sender user {sender_id} not found", "halt": True})
        
        # Validate recipient exists
        if str(recipient_id) not in users:
            return json.dumps({"error": f"Recipient user {recipient_id} not found", "halt": True})
        
        # Validate delivery_method
        valid_delivery_methods = ["email", "sms", "phone", "chat", "dashboard_notification"]
        if delivery_method not in valid_delivery_methods:
            return json.dumps({"error": f"Invalid delivery_method. Must be one of {valid_delivery_methods}", "halt": True})
        
        # Validate delivery_status
        valid_statuses = ["pending", "sent", "delivered", "failed"]
        if delivery_status not in valid_statuses:
            return json.dumps({"error": f"Invalid delivery_status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate recipient_type if provided
        if recipient_type:
            valid_recipient_types = ["client_contacts", "executive_team", "technical_team", "all_stakeholders"]
            if recipient_type not in valid_recipient_types:
                return json.dumps({"error": f"Invalid recipient_type. Must be one of {valid_recipient_types}", "halt": True})
        
        communication_id = generate_id(communications)
        timestamp = "2025-10-01T00:00:00"
        
        new_communication = {
            "communication_id": communication_id,
            "incident_id": incident_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "recipient_type": recipient_type,
            "communication_type": communication_type,
            "delivery_method": delivery_method,
            "delivery_status": delivery_status,
            "sent_at": sent_at if sent_at and delivery_status == 'sent' else None,
            "created_at": timestamp
        }
        
        communications[communication_id] = new_communication
        return json.dumps({"communication_id": communication_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_communication",
                "description": "Record a communication related to an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "sender_id": {"type": "string", "description": "ID of sender user"},
                        "recipient_id": {"type": "string", "description": "ID of recipient user"},
                        "communication_type": {"type": "string", "description": "Type of communication"},
                        "delivery_method": {"type": "string", "description": "Method of delivery (email, sms, phone, chat, dashboard_notification)"},
                        "delivery_status": {"type": "string", "description": "Delivery status (pending, sent, delivered, failed), defaults to pending"},
                        "recipient_type": {"type": "string", "description": "Type of recipient (client_contacts, executive_team, technical_team, all_stakeholders)"},
                        "sent_at": {"type": "string", "description": "When communication was sent"}
                    },
                    "required": ["incident_id", "sender_id", "recipient_id", "communication_type", "delivery_method"]
                }
            }
        }
