import json
from typing import Any, Dict, Optional

class AddMetric:
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, metric_type: str,
               calculated_value_minutes: float, recorded_by_user: str,
               target_minutes: Optional[float] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        performance_metrics = data.get("performance_metrics", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if str(recorded_by_user) not in users:
            return json.dumps({"error": f"User {recorded_by_user} not found", "halt": True})
        
        # Validate metric_type
        valid_metric_types = ["response_time", "resolution_time", "detection_time", "escalation_time"]
        if metric_type not in valid_metric_types:
            return json.dumps({"error": f"Invalid metric_type. Must be one of {valid_metric_types}", "halt": True})
        
        metric_id = generate_id(performance_metrics)
        timestamp = "2025-10-01T00:00:00"
        
        new_metric = {
            "metric_id": metric_id,
            "incident_id": incident_id,
            "metric_type": metric_type,
            "calculated_value_minutes": int(calculated_value_minutes),
            "target_minutes": int(target_minutes) if target_minutes else None,
            "recorded_by_user": recorded_by_user,
            "recorded_at": timestamp,
            "created_at": timestamp
        }
        
        performance_metrics[metric_id] = new_metric
        
        # Calculate summary values for this incident
        calculated_values = {}
        for metric in performance_metrics.values():
            if metric.get("incident_id") == incident_id:
                m_type = metric.get("metric_type")
                if m_type not in calculated_values:
                    calculated_values[m_type] = []
                calculated_values[m_type].append(metric.get("calculated_value_minutes"))
        
        return json.dumps({"metric_id": metric_id, "calculated_values": calculated_values, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_metric",
                "description": "Log a performance metric for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "metric_type": {"type": "string", "description": "Type of metric being recorded (response_time, resolution_time, detection_time, escalation_time)"},
                        "calculated_value_minutes": {"type": "number", "description": "Calculated metric value in minutes"},
                        "recorded_by_user": {"type": "string", "description": "User recording the metric"},
                        "target_minutes": {"type": "number", "description": "Target value in minutes if specified"}
                    },
                    "required": ["incident_id", "metric_type", "calculated_value_minutes", "recorded_by_user"]
                }
            }
        }
