import json
from typing import Any, Dict, Optional

class AddKbArticle:
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, article_type: str, category: str,
               created_by_user: str, incident_id: Optional[str] = None,
               reviewer_user: Optional[str] = None, status: Optional[str] = 'draft') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        kb_articles = data.get("knowledge_base_articles", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        
        # Validate created_by user exists
        if str(created_by_user) not in users:
            return json.dumps({"error": f"User {created_by_user} not found", "halt": True})
        
        # Validate reviewer user if provided
        if reviewer_user and str(reviewer_user) not in users:
            return json.dumps({"error": f"Reviewer user {reviewer_user} not found", "halt": True})
        
        # Validate incident if provided
        if incident_id and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate article_type
        valid_article_types = ["troubleshooting", "resolution_procedure", "prevention_guide", "faq"]
        if article_type not in valid_article_types:
            return json.dumps({"error": f"Invalid article_type. Must be one of {valid_article_types}", "halt": True})
        
        # Validate category
        valid_categories = ["technical", "process", "communication", "escalation"]
        if category not in valid_categories:
            return json.dumps({"error": f"Invalid category. Must be one of {valid_categories}", "halt": True})
        
        # Validate status
        valid_statuses = ["draft", "under_review", "archived", "published"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        article_id = generate_id(kb_articles)
        timestamp = "2025-10-01T00:00:00"
        
        new_article = {
            "article_id": article_id,
            "incident_id": incident_id,
            "title": title,
            "article_type": article_type,
            "category": category,
            "created_by_user": created_by_user,
            "reviewer_user": reviewer_user,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        kb_articles[article_id] = new_article
        return json.dumps({"article_id": article_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_kb_article",
                "description": "Record a knowledge base article",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Article title"},
                        "article_type": {"type": "string", "description": "Type of article (troubleshooting, resolution_procedure, prevention_guide, faq)"},
                        "category": {"type": "string", "description": "Article category (technical, process, communication, escalation)"},
                        "created_by_user": {"type": "string", "description": "User creating the article"},
                        "incident_id": {"type": "string", "description": "Related incident ID if applicable"},
                        "reviewer_user": {"type": "string", "description": "User assigned to review"},
                        "status": {"type": "string", "description": "Article status (draft, under_review, archived, published), defaults to 'draft'"}
                    },
                    "required": ["title", "article_type", "category", "created_by_user"]
                }
            }
        }
