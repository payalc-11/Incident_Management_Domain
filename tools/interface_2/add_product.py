import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddProduct(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_name: str, product_type: str,
               version: Optional[str] = None, support_vendor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        products = data.get("products", {})
        vendors = data.get("vendors", {})
        
        # Check for unique product_name
        for product in products.values():
            if product.get("product_name") == product_name:
                return json.dumps({"error": f"Product name {product_name} already exists", "halt": True})
        
        # Validate vendor if provided
        if support_vendor_id and support_vendor_id not in vendors:
            return json.dumps({"error": f"Vendor {support_vendor_id} not found", "halt": True})
        
        product_id = str(generate_id(products))
        timestamp = "2025-10-01T00:00:00"
        
        new_product = {
            "product_id": product_id,
            "product_name": product_name,
            "product_type": product_type,
            "version": version,
            "support_vendor_id": support_vendor_id,
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        products[product_id] = new_product
        return json.dumps({"product_id": product_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_product",
                "description": "Add a new product to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string", "description": "Unique name of the product"},
                        "product_type": {"type": "string", "description": "Type of product"},
                        "version": {"type": "string", "description": "Product version"},
                        "support_vendor_id": {"type": "string", "description": "ID of supporting vendor"}
                    },
                    "required": ["product_name", "product_type"]
                }
            }
        }
