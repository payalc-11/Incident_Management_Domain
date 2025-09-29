import json
from typing import Any, Dict, Optional

class GenerateIncidentReport:
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, report_type: str,
               generated_by_user: str, status: Optional[str] = 'completed') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        incident_reports = data.get("incident_reports", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if str(generated_by_user) not in users:
            return json.dumps({"error": f"User {generated_by_user} not found", "halt": True})
        
        # Validate report_type
        valid_report_types = ["executive_summary", "compliance_report", "technical_details", "business_impact", "post_mortem"]
        if report_type not in valid_report_types:
            return json.dumps({"error": f"Invalid report_type. Must be one of {valid_report_types}", "halt": True})
        
        # Validate status
        valid_statuses = ["completed", "draft", "published"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        report_id = generate_id(incident_reports)
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": report_id,
            "incident_id": incident_id,
            "report_type": report_type,
            "generated_by_user": generated_by_user,
            "status": status,
            "generated_at": timestamp,
            "created_at": timestamp
        }
        
        incident_reports[report_id] = new_report
        return json.dumps({"report_id": report_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_incident_report",
                "description": "Generate a report for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "report_type": {"type": "string", "description": "Type of report to generate (executive_summary, compliance_report, technical_details, business_impact, post_mortem)"},
                        "generated_by_user": {"type": "string", "description": "User generating the report"},
                        "status": {"type": "string", "description": "Report status (completed, draft, published), defaults to 'completed'"}
                    },
                    "required": ["incident_id", "report_type", "generated_by_user"]
                }
            }
        }
