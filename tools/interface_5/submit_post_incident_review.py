import json
from typing import Any, Dict, Optional

class SubmitPostIncidentReview:
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, facilitator_user: str,
               scheduled_date: str, overall_rating: str, status: Optional[str] = 'scheduled') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        post_incident_reviews = data.get("post_incident_reviews", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate facilitator user exists
        if str(facilitator_user) not in users:
            return json.dumps({"error": f"Facilitator user {facilitator_user} not found", "halt": True})
        
        # Validate overall_rating
        valid_ratings = ["excellent", "good", "satisfactory", "needs_improvement", "poor"]
        if overall_rating not in valid_ratings:
            return json.dumps({"error": f"Invalid overall_rating. Must be one of {valid_ratings}", "halt": True})
        
        # Validate status
        valid_statuses = ["scheduled", "completed", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        review_id = generate_id(post_incident_reviews)
        timestamp = "2025-10-01T00:00:00"
        
        new_review = {
            "review_id": review_id,
            "incident_id": incident_id,
            "facilitator_user": facilitator_user,
            "scheduled_date": scheduled_date,
            "overall_rating": overall_rating,
            "status": status,
            "completed_at": None,
            "created_at": timestamp
        }
        
        post_incident_reviews[review_id] = new_review
        return json.dumps({"review_id": review_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_post_incident_review",
                "description": "Submit a post-incident review",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "facilitator_user": {"type": "string", "description": "User facilitating the review"},
                        "scheduled_date": {"type": "string", "description": "Date when PIR is scheduled (YYYY-MM-DD)"},
                        "overall_rating": {"type": "string", "description": "Overall rating of incident response (excellent, good, satisfactory, needs_improvement, poor)"},
                        "status": {"type": "string", "description": "PIR status (scheduled, completed, cancelled), defaults to 'scheduled'"}
                    },
                    "required": ["incident_id", "facilitator_user", "scheduled_date", "overall_rating"]
                }
            }
        }
