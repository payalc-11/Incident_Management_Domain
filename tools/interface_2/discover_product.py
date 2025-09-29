import json
from typing import Any, Dict, Optional

class DiscoverProduct:
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: Optional[str] = None,
               product_name: Optional[str] = None, product_type: Optional[str] = None,
               support_vendor_id: Optional[str] = None) -> str:
        
        products = data.get("products", {})
        results = []
        
        for product in products.values():
            if product_id and str(product.get("product_id")) != str(product_id):
                continue
            if product_name and product_name.lower() not in product.get("poduct_name", "").lower():
                continue
            if product_type and product.get("product_type") != product_type:
                continue
            if support_vendor_id and product.get("support_vendor_id") != support_vendor_id:
                continue
            results.append(product)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_product",
                "description": "Discover products with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string", "description": "Filter by product ID"},
                        "product_name": {"type": "string", "description": "Filter by product name (partial match)"},
                        "product_type": {"type": "string", "description": "Filter by product type"},
                        "support_vendor_id": {"type": "string", "description": "Filter by supporting vendor"}
                    },
                    "required": []
                }
            }
        }
