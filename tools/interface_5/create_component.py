import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateComponent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], component_name: str, component_type: str,
               environment: str, product_id: Optional[str] = None,
               location: Optional[str] = None, port_number: Optional[int] = None,
               operational_status: Optional[str] = 'operational') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        components = data.get("infrastructure_components", {})
        products = data.get("products", {})
        
        # Validate environment
        valid_environments = ["production", "staging", "development", "testing"]
        if environment not in valid_environments:
            return json.dumps({"error": f"Invalid environment. Must be one of {valid_environments}", "halt": True})
        
        # Validate operational_status
        valid_statuses = ["operational", "degraded", "offline", "maintenance"]
        if operational_status not in valid_statuses:
            return json.dumps({"error": f"Invalid operational_status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique component_name
        for component in components.values():
            if component.get("component_name") == component_name:
                return json.dumps({"error": f"Component name {component_name} already exists", "halt": True})
        
        # Validate product if provided
        if product_id and product_id not in products:
            return json.dumps({"error": f"Product {product_id} not found", "halt": True})
        
        component_id = str(generate_id(components))
        timestamp = "2025-10-01T00:00:00"
        
        new_component = {
            "component_id": component_id,
            "component_name": component_name,
            "component_type": component_type,
            "product_id": product_id,
            "environment": environment,
            "location": location,
            "port_number": str(port_number) if port_number else None,
            "operational_status": operational_status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        components[component_id] = new_component
        return json.dumps({"component_id": component_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_component",
                "description": "Add a new infrastructure component to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "component_name": {"type": "string", "description": "Unique name of the component"},
                        "component_type": {"type": "string", "description": "Type of component"},
                        "environment": {"type": "string", "description": "Environment where component operates (production/staging/development/testing)"},
                        "product_id": {"type": "string", "description": "Associated product ID"},
                        "location": {"type": "string", "description": "Physical or logical location"},
                        "port_number": {"type": "integer", "description": "Network port number"},
                        "operational_status": {"type": "string", "description": "Status (operational/degraded/offline/maintenance)"}
                    },
                    "required": ["component_name", "component_type", "environment"]
                }
            }
        }
