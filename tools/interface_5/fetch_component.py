import json
from typing import Any, Dict, Optional

class FetchComponent:
    @staticmethod
    def invoke(data: Dict[str, Any], component_id: Optional[str] = None,
               component_name: Optional[str] = None, component_type: Optional[str] = None,
               product_id: Optional[str] = None, environment: Optional[str] = None,
               operational_status: Optional[str] = None) -> str:
        
        components = data.get("infrastructure_components", {})
        results = []
        
        for component in components.values():
            if component_id and str(component.get("component_id")) != str(component_id):
                continue
            if component_name and component_name.lower() not in component.get("component_name", "").lower():
                continue
            if component_type and component.get("component_type") != component_type:
                continue
            if product_id and component.get("product_id") != product_id:
                continue
            if environment and component.get("environment") != environment:
                continue
            if operational_status and component.get("operational_status") != operational_status:
                continue
            results.append(component)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_component",
                "description": "Discover infrastructure components with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "component_id": {"type": "string", "description": "Filter by component ID"},
                        "component_name": {"type": "string", "description": "Filter by component name (partial match)"},
                        "component_type": {"type": "string", "description": "Filter by component type"},
                        "product_id": {"type": "string", "description": "Filter by associated product"},
                        "environment": {"type": "string", "description": "Filter by environment (production, staging, development, testing)"},
                        "operational_status": {"type": "string", "description": "Filter by operational status (operational, degraded, offline, maintenance)"}
                    },
                    "required": []
                }
            }
        }
