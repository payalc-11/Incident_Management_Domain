#!/bin/bash

# Create directory for tools if it doesn't exist
mkdir -p tools

# Tool 1: create_client
cat > tools/create_client.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateClient(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_name: str, registration_number: str,
               contact_email: str, client_type: str, country: Optional[str] = None,
               industry: Optional[str] = None, status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        clients = data.get("clients", {})
        
        # Validate client_type
        valid_client_types = ["enterprise", "mid_market", "small_business", "startup"]
        if client_type not in valid_client_types:
            return json.dumps({"error": f"Invalid client_type. Must be one of {valid_client_types}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique registration_number
        for client in clients.values():
            if client.get("registration_number") == registration_number:
                return json.dumps({"error": f"Registration number {registration_number} already exists", "halt": True})
        
        # Check for unique contact_email
        for client in clients.values():
            if client.get("contact_email") == contact_email:
                return json.dumps({"error": f"Contact email {contact_email} already exists", "halt": True})
        
        client_id = str(generate_id(clients))
        timestamp = "2025-10-01T00:00:00"
        
        new_client = {
            "client_id": client_id,
            "client_name": client_name,
            "registration_number": registration_number,
            "contact_email": contact_email,
            "client_type": client_type,
            "industry": industry,
            "country": country,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        clients[client_id] = new_client
        return json.dumps({"client_id": client_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_client",
                "description": "Create a new client in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_name": {"type": "string", "description": "Name of the client"},
                        "registration_number": {"type": "string", "description": "Unique registration number"},
                        "contact_email": {"type": "string", "description": "Unique contact email address"},
                        "client_type": {"type": "string", "description": "Type of client (enterprise/mid_market/small_business/startup)"},
                        "country": {"type": "string", "description": "Country of the client"},
                        "industry": {"type": "string", "description": "Industry sector of the client"},
                        "status": {"type": "string", "description": "Status of the client (active/inactive/suspended)"}
                    },
                    "required": ["client_name", "registration_number", "contact_email", "client_type"]
                }
            }
        }
EOF

# Tool 2: update_client
cat > tools/update_client.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateClient(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str, change_set: Dict[str, Any],
               registration_number: Optional[str] = None, contact_email: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        clients = data.get("clients", {})
        
        # Validate client exists
        if client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if registration_number:
            change_set["registration_number"] = registration_number
        if contact_email:
            change_set["contact_email"] = contact_email
        if status:
            change_set["status"] = status
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["active", "inactive", "suspended"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check unique constraints
        if "registration_number" in change_set:
            for cid, client in clients.items():
                if cid != client_id and client.get("registration_number") == change_set["registration_number"]:
                    return json.dumps({"error": f"Registration number {change_set['registration_number']} already exists", "halt": True})
        
        if "contact_email" in change_set:
            for cid, client in clients.items():
                if cid != client_id and client.get("contact_email") == change_set["contact_email"]:
                    return json.dumps({"error": f"Contact email {change_set['contact_email']} already exists", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            clients[client_id][key] = value
        
        clients[client_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(clients[client_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_client",
                "description": "Update an existing client's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string", "description": "ID of the client to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "registration_number": {"type": "string", "description": "New unique registration number if being updated"},
                        "contact_email": {"type": "string", "description": "New unique contact email if being updated"},
                        "status": {"type": "string", "description": "New status (active/inactive/suspended)"}
                    },
                    "required": ["client_id", "change_set"]
                }
            }
        }
EOF

# Tool 3: register_user
cat > tools/register_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class RegisterUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, email: str, role: str,
               department: Optional[str] = None, client_id: Optional[str] = None,
               vendor_id: Optional[str] = None, timezone: Optional[str] = 'UTC',
               status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        clients = data.get("clients", {})
        vendors = data.get("vendors", {})
        
        # Validate role
        valid_roles = ["system_administrator", "incident_manager", "technical_support", 
                      "account_manager", "executive", "client_contact", "vendor_contact"]
        if role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "on_leave"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique email
        for user in users.values():
            if user.get("email") == email:
                return json.dumps({"error": f"Email {email} already exists", "halt": True})
        
        # Validate client_id if provided
        if client_id and client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        
        # Validate vendor_id if provided
        if vendor_id and vendor_id not in vendors:
            return json.dumps({"error": f"Vendor {vendor_id} not found", "halt": True})
        
        user_id = str(generate_id(users))
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "department": department,
            "client_id": client_id,
            "vendor_id": vendor_id,
            "timezone": timezone,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_user",
                "description": "Register a new user in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the user"},
                        "email": {"type": "string", "description": "Unique email address"},
                        "role": {"type": "string", "description": "User role (system_administrator/incident_manager/technical_support/account_manager/executive/client_contact/vendor_contact)"},
                        "department": {"type": "string", "description": "Department of the user"},
                        "client_id": {"type": "string", "description": "Associated client ID"},
                        "vendor_id": {"type": "string", "description": "Associated vendor ID"},
                        "timezone": {"type": "string", "description": "User timezone (defaults to UTC)"},
                        "status": {"type": "string", "description": "User status (active/inactive/on_leave)"}
                    },
                    "required": ["name", "email", "role"]
                }
            }
        }
EOF

# Tool 4: update_user
cat > tools/update_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, change_set: Dict[str, Any],
               role: Optional[str] = None, status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        
        # Validate user exists
        if user_id not in users:
            return json.dumps({"error": f"User {user_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if role:
            change_set["role"] = role
        if status:
            change_set["status"] = status
        
        # Validate role if being updated
        if "role" in change_set:
            valid_roles = ["system_administrator", "incident_manager", "technical_support",
                          "account_manager", "executive", "client_contact", "vendor_contact"]
            if change_set["role"] not in valid_roles:
                return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}", "halt": True})
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["active", "inactive", "on_leave"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check unique email if being updated
        if "email" in change_set:
            for uid, user in users.items():
                if uid != user_id and user.get("email") == change_set["email"]:
                    return json.dumps({"error": f"Email {change_set['email']} already exists", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            users[user_id][key] = value
        
        users[user_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(users[user_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user",
                "description": "Update an existing user's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "role": {"type": "string", "description": "New role assignment"},
                        "status": {"type": "string", "description": "New status (active/inactive/on_leave)"}
                    },
                    "required": ["user_id", "change_set"]
                }
            }
        }
EOF

# Tool 5: create_vendor
cat > tools/create_vendor.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateVendor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_name: str, vendor_email: str,
               vendor_phone: str, vendor_type: str, status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        vendors = data.get("vendors", {})
        
        # Validate vendor_type
        valid_vendor_types = ["technology_provider", "infrastructure_provider", "security_provider",
                             "consulting_services", "maintenance_services", "cloud_provider", "payment_processor"]
        if vendor_type not in valid_vendor_types:
            return json.dumps({"error": f"Invalid vendor_type. Must be one of {valid_vendor_types}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Check for unique vendor_name
        for vendor in vendors.values():
            if vendor.get("vendor_name") == vendor_name:
                return json.dumps({"error": f"Vendor name {vendor_name} already exists", "halt": True})
        
        # Check for unique contact_email
        for vendor in vendors.values():
            if vendor.get("contact_email") == vendor_email:
                return json.dumps({"error": f"Contact email {vendor_email} already exists", "halt": True})
        
        # Check for unique contact_phone
        for vendor in vendors.values():
            if vendor.get("contact_phone") == vendor_phone:
                return json.dumps({"error": f"Contact phone {vendor_phone} already exists", "halt": True})
        
        vendor_id = str(generate_id(vendors))
        timestamp = "2025-10-01T00:00:00"
        
        new_vendor = {
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "vendor_type": vendor_type,
            "contact_email": vendor_email,
            "contact_phone": vendor_phone,
            "status": status,
            "created_at": timestamp
        }
        
        vendors[vendor_id] = new_vendor
        return json.dumps({"vendor_id": vendor_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_vendor",
                "description": "Create a new vendor in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_name": {"type": "string", "description": "Unique name of the vendor"},
                        "vendor_email": {"type": "string", "description": "Unique email address"},
                        "vendor_phone": {"type": "string", "description": "Unique phone number"},
                        "vendor_type": {"type": "string", "description": "Type of vendor (technology_provider/infrastructure_provider/security_provider/consulting_services/maintenance_services/cloud_provider/payment_processor)"},
                        "status": {"type": "string", "description": "Vendor status (active/inactive/suspended)"}
                    },
                    "required": ["vendor_name", "vendor_email", "vendor_phone", "vendor_type"]
                }
            }
        }
EOF

# Tool 6: add_product
cat > tools/add_product.py << 'EOF'
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
EOF

# Tool 7: add_component
cat > tools/add_component.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddComponent(Tool):
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
                "name": "add_component",
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
EOF

# Tool 8: create_client_subscription
cat > tools/create_client_subscription.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateClientSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str, product_id: str,
               subscription_type: str, sla_tier: str, start_date: str,
               end_date: str, rto_hours: Optional[int] = None,
               status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        subscriptions = data.get("subscriptions", {})
        clients = data.get("clients", {})
        products = data.get("products", {})
        
        # Validate client exists
        if client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        
        # Validate product exists
        if product_id not in products:
            return json.dumps({"error": f"Product {product_id} not found", "halt": True})
        
        # Validate subscription_type
        valid_subscription_types = ["trial", "limited_service", "full_service", "custom"]
        if subscription_type not in valid_subscription_types:
            return json.dumps({"error": f"Invalid subscription_type. Must be one of {valid_subscription_types}", "halt": True})
        
        # Validate sla_tier
        valid_sla_tiers = ["basic", "standard", "premium"]
        if sla_tier not in valid_sla_tiers:
            return json.dumps({"error": f"Invalid sla_tier. Must be one of {valid_sla_tiers}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "cancelled", "expired"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        subscription_id = str(generate_id(subscriptions))
        timestamp = "2025-10-01T00:00:00"
        
        new_subscription = {
            "subscription_id": subscription_id,
            "client_id": client_id,
            "product_id": product_id,
            "subscription_type": subscription_type,
            "sla_tier": sla_tier,
            "rto_hours": rto_hours,
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        subscriptions[subscription_id] = new_subscription
        return json.dumps({"subscription_id": subscription_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_client_subscription",
                "description": "Create a new subscription for a client",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string", "description": "ID of the client"},
                        "product_id": {"type": "string", "description": "ID of the product"},
                        "subscription_type": {"type": "string", "description": "Type of subscription (trial/limited_service/full_service/custom)"},
                        "sla_tier": {"type": "string", "description": "SLA tier (basic/standard/premium)"},
                        "start_date": {"type": "string", "description": "Subscription start date (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "Subscription end date (YYYY-MM-DD)"},
                        "rto_hours": {"type": "integer", "description": "Recovery time objective in hours"},
                        "status": {"type": "string", "description": "Subscription status (active/inactive/cancelled/expired)"}
                    },
                    "required": ["client_id", "product_id", "subscription_type", "sla_tier", "start_date", "end_date"]
                }
            }
        }
EOF

# Tool 9: create_sla_record
cat > tools/create_sla_record.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateSlaRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, response_time_minutes: int,
               resolution_time_hours: int, availability_percentage: Optional[float] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        slas = data.get("service_level_agreements", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if subscription_id not in subscriptions:
            return json.dumps({"error": f"Subscription {subscription_id} not found", "halt": True})
        
        sla_id = str(generate_id(slas))
        timestamp = "2025-10-01T00:00:00"
        
        new_sla = {
            "sla_id": sla_id,
            "subscription_id": subscription_id,
            "severity_level": None,
            "response_time_minutes": response_time_minutes,
            "resolution_time_hours": resolution_time_hours,
            "availability_percentage": availability_percentage,
            "created_at": timestamp
        }
        
        slas[sla_id] = new_sla
        return json.dumps({"sla_id": sla_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_sla_record",
                "description": "Create an SLA record for a subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription"},
                        "response_time_minutes": {"type": "integer", "description": "Response time in minutes"},
                        "resolution_time_hours": {"type": "integer", "description": "Resolution time in hours"},
                        "availability_percentage": {"type": "number", "description": "Availability percentage target"}
                    },
                    "required": ["subscription_id", "response_time_minutes", "resolution_time_hours"]
                }
            }
        }
EOF

# Tool 10: manage_sla_record
cat > tools/manage_sla_record.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageSlaRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, severity_level: str,
               response_time_minutes: int, resolution_time_hours: int,
               availability_percentage: Optional[float] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        slas = data.get("service_level_agreements", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if subscription_id not in subscriptions:
            return json.dumps({"error": f"Subscription {subscription_id} not found", "halt": True})
        
        # Validate severity_level
        valid_severity_levels = ["P1", "P2", "P3", "P4"]
        if severity_level not in valid_severity_levels:
            return json.dumps({"error": f"Invalid severity_level. Must be one of {valid_severity_levels}", "halt": True})
        
        sla_id = str(generate_id(slas))
        timestamp = "2025-10-01T00:00:00"
        
        new_sla = {
            "sla_id": sla_id,
            "subscription_id": subscription_id,
            "severity_level": severity_level,
            "response_time_minutes": response_time_minutes,
            "resolution_time_hours": resolution_time_hours,
            "availability_percentage": availability_percentage,
            "created_at": timestamp
        }
        
        slas[sla_id] = new_sla
        return json.dumps({"sla_id": sla_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_sla_record",
                "description": "Manage SLA record with severity levels for a subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription"},
                        "severity_level": {"type": "string", "description": "Severity level (P1/P2/P3/P4)"},
                        "response_time_minutes": {"type": "integer", "description": "Response time in minutes"},
                        "resolution_time_hours": {"type": "integer", "description": "Resolution time in hours"},
                        "availability_percentage": {"type": "number", "description": "Availability percentage target"}
                    },
                    "required": ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_hours"]
                }
            }
        }
EOF

# Tool 11: report_incident
cat > tools/report_incident.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ReportIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, category: str, severity: str,
               impact_level: str, urgency_level: str, client_id: str,
               component_id: str, reporter_user_id: str, detection_timestamp: str,
               status: Optional[str] = 'open', assigned_to_user_id: Optional[str] = None,
               resolution_timestamp: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        clients = data.get("clients", {})
        components = data.get("infrastructure_components", {})
        users = data.get("users", {})
        
        # Validate severity
        valid_severities = ["P1", "P2", "P3", "P4"]
        if severity not in valid_severities:
            return json.dumps({"error": f"Invalid severity. Must be one of {valid_severities}", "halt": True})
        
        # Validate levels
        valid_levels = ["low", "medium", "high", "critical"]
        if impact_level not in valid_levels:
            return json.dumps({"error": f"Invalid impact_level. Must be one of {valid_levels}", "halt": True})
        if urgency_level not in valid_levels:
            return json.dumps({"error": f"Invalid urgency_level. Must be one of {valid_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate entities exist
        if client_id not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        if component_id not in components:
            return json.dumps({"error": f"Component {component_id} not found", "halt": True})
        if reporter_user_id not in users:
            return json.dumps({"error": f"Reporter user {reporter_user_id} not found", "halt": True})
        if assigned_to_user_id and assigned_to_user_id not in users:
            return json.dumps({"error": f"Assigned user {assigned_to_user_id} not found", "halt": True})
        
        incident_id = str(generate_id(incidents))
        timestamp = "2025-10-01T00:00:00"
        
        new_incident = {
            "incident_id": incident_id,
            "title": title,
            "category": category,
            "severity": severity,
            "impact_level": impact_level,
            "urgency_level": urgency_level,
            "status": status,
            "client_id": client_id,
            "component_id": component_id,
            "reporter_user_id": reporter_user_id,
            "assigned_to_user_id": assigned_to_user_id,
            "detection_timestamp": detection_timestamp,
            "resolution_timestamp": resolution_timestamp,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        incidents[incident_id] = new_incident
        return json.dumps({"incident_id": incident_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "report_incident",
                "description": "Report a new incident in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Incident title"},
                        "category": {"type": "string", "description": "Incident category"},
                        "severity": {"type": "string", "description": "Severity level (P1/P2/P3/P4)"},
                        "impact_level": {"type": "string", "description": "Impact level (low/medium/high/critical)"},
                        "urgency_level": {"type": "string", "description": "Urgency level (low/medium/high/critical)"},
                        "client_id": {"type": "string", "description": "ID of affected client"},
                        "component_id": {"type": "string", "description": "ID of affected component"},
                        "reporter_user_id": {"type": "string", "description": "ID of user reporting the incident"},
                        "detection_timestamp": {"type": "string", "description": "When incident was detected"},
                        "status": {"type": "string", "description": "Incident status (open/investigating/in_progress/resolved/closed)"},
                        "assigned_to_user_id": {"type": "string", "description": "ID of assigned user"},
                        "resolution_timestamp": {"type": "string", "description": "When incident was resolved"}
                    },
                    "required": ["title", "category", "severity", "impact_level", "urgency_level", "client_id", "component_id", "reporter_user_id", "detection_timestamp"]
                }
            }
        }
EOF

# Tool 12: update_incident
cat > tools/update_incident.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, change_set: Dict[str, Any],
               status: Optional[str] = None, assigned_to_user_id: Optional[str] = None,
               resolution_timestamp: Optional[str] = None) -> str:
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if status:
            change_set["status"] = status
        if assigned_to_user_id:
            change_set["assigned_to_user_id"] = assigned_to_user_id
        if resolution_timestamp:
            change_set["resolution_timestamp"] = resolution_timestamp
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate assigned user if being updated
        if "assigned_to_user_id" in change_set and change_set["assigned_to_user_id"]:
            if change_set["assigned_to_user_id"] not in users:
                return json.dumps({"error": f"Assigned user {change_set['assigned_to_user_id']} not found", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            incidents[incident_id][key] = value
        
        incidents[incident_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(incidents[incident_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_incident",
                "description": "Update an existing incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "status": {"type": "string", "description": "New status (open/investigating/in_progress/resolved/closed)"},
                        "assigned_to_user_id": {"type": "string", "description": "New assignee"},
                        "resolution_timestamp": {"type": "string", "description": "Resolution timestamp"}
                    },
                    "required": ["incident_id", "change_set"]
                }
            }
        }
EOF

# Tool 13: log_incident_update
cat > tools/log_incident_update.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class LogIncidentUpdate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, update_type: str,
               update_details: Dict[str, Any], updated_by_user: str,
               update_timestamp: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incident_updates = data.get("incident_updates", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if updated_by_user not in users:
            return json.dumps({"error": f"User {updated_by_user} not found", "halt": True})
        
        update_id = str(generate_id(incident_updates))
        
        # Extract field changes from update_details
        field_changed = update_details.get("field_changed", "multiple_fields")
        old_value = update_details.get("old_value", "")
        new_value = update_details.get("new_value", "")
        
        new_update = {
            "update_id": update_id,
            "incident_id": incident_id,
            "updated_by_user": updated_by_user,
            "update_type": update_type,
            "field_changed": field_changed,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": update_timestamp
        }
        
        incident_updates[update_id] = new_update
        return json.dumps({"update_id": update_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_incident_update",
                "description": "Log an update to an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "update_type": {"type": "string", "description": "Type of update"},
                        "update_details": {"type": "object", "description": "Details of the update"},
                        "updated_by_user": {"type": "string", "description": "User making the update"},
                        "update_timestamp": {"type": "string", "description": "When update was made"}
                    },
                    "required": ["incident_id", "update_type", "update_details", "updated_by_user", "update_timestamp"]
                }
            }
        }
EOF

# Tool 14: submit_escalation
cat > tools/submit_escalation.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SubmitEscalation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, escalated_by_user: str,
               escalated_to_user: str, escalation_level: str, escalated_at: str,
               reason: Optional[str] = None, status: Optional[str] = 'active',
               resolved_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        escalations = data.get("incident_escalations", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate users exist
        if escalated_by_user not in users:
            return json.dumps({"error": f"User {escalated_by_user} not found", "halt": True})
        if escalated_to_user not in users:
            return json.dumps({"error": f"User {escalated_to_user} not found", "halt": True})
        
        # Validate escalation_level
        valid_levels = ["management", "technical", "executive", "vendor"]
        if escalation_level not in valid_levels:
            return json.dumps({"error": f"Invalid escalation_level. Must be one of {valid_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "resolved", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        escalation_id = str(generate_id(escalations))
        timestamp = "2025-10-01T00:00:00"
        
        new_escalation = {
            "escalation_id": escalation_id,
            "incident_id": incident_id,
            "escalated_by_user": escalated_by_user,
            "escalated_to_user": escalated_to_user,
            "escalation_level": escalation_level,
            "reason": reason,
            "status": status,
            "escalated_at": escalated_at,
            "resolved_at": resolved_at,
            "created_at": timestamp
        }
        
        escalations[escalation_id] = new_escalation
        return json.dumps({"escalation_id": escalation_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_escalation",
                "description": "Submit an escalation for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident to escalate"},
                        "escalated_by_user": {"type": "string", "description": "User initiating escalation"},
                        "escalated_to_user": {"type": "string", "description": "Target user for escalation"},
                        "escalation_level": {"type": "string", "description": "Level of escalation (management/technical/executive/vendor)"},
                        "escalated_at": {"type": "string", "description": "Timestamp of escalation"},
                        "reason": {"type": "string", "description": "Reason for escalation"},
                        "status": {"type": "string", "description": "Escalation status (active/resolved/cancelled)"},
                        "resolved_at": {"type": "string", "description": "When escalation was resolved"}
                    },
                    "required": ["incident_id", "escalated_by_user", "escalated_to_user", "escalation_level", "escalated_at"]
                }
            }
        }
EOF

# Tool 15: create_ticket
cat > tools/create_ticket.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, title: str,
               issued_by_user: str, status: Optional[str] = 'open') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        problem_tickets = data.get("problem_tickets", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        
        # Validate incident exists
        if incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if issued_by_user not in users:
            return json.dumps({"error": f"User {issued_by_user} not found", "halt": True})
        
        # Validate status
        valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        problem_id = str(generate_id(problem_tickets))
        timestamp = "2025-10-01T00:00:00"
        
        new_ticket = {
            "problem_id": problem_id,
            "incident_id": incident_id,
            "title": title,
            "status": status,
            "issued_by_user": issued_by_user,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        problem_tickets[problem_id] = new_ticket
        return json.dumps({"ticket_id": problem_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_ticket",
                "description": "Create a problem ticket for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Parent incident ID"},
                        "title": {"type": "string", "description": "Problem ticket title"},
                        "issued_by_user": {"type": "string", "description": "User creating the ticket"},
                        "status": {"type": "string", "description": "Ticket status (open/investigating/in_progress/resolved/closed)"}
                    },
                    "required": ["incident_id", "title", "issued_by_user"]
                }
            }
        }
EOF

# Tool 16: update_ticket
cat > tools/update_ticket.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticket_id: str, change_set: Dict[str, Any],
               status: Optional[str] = None) -> str:
        
        problem_tickets = data.get("problem_tickets", {})
        
        # Validate ticket exists
        if ticket_id not in problem_tickets:
            return json.dumps({"error": f"Ticket {ticket_id} not found", "halt": True})
        
        # Update change_set with optional parameter if provided
        if status:
            change_set["status"] = status
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["open", "investigating", "in_progress", "resolved", "closed"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            problem_tickets[ticket_id][key] = value
        
        problem_tickets[ticket_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(problem_tickets[ticket_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_ticket",
                "description": "Update a problem ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "ID of the ticket to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "status": {"type": "string", "description": "New status (open/investigating/in_progress/resolved/closed)"}
                    },
                    "required": ["ticket_id", "change_set"]
                }
            }
        }
EOF

# Tool 17: create_workorder
cat > tools/create_workorder.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateWorkorder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, work_type: str, created_by_user: str,
               incident_id: Optional[str] = None, change_id: Optional[str] = None,
               problem_id: Optional[str] = None, assigned_to_user: Optional[str] = None,
               status: Optional[str] = 'created') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        work_orders = data.get("work_orders", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        change_requests = data.get("change_requests", {})
        problem_tickets = data.get("problem_tickets", {})
        
        # Validate user exists
        if created_by_user not in users:
            return json.dumps({"error": f"User {created_by_user} not found", "halt": True})
        
        # Validate assigned user if provided
        if assigned_to_user and assigned_to_user not in users:
            return json.dumps({"error": f"Assigned user {assigned_to_user} not found", "halt": True})
        
        # Validate related entities if provided
        if incident_id and incident_id not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if change_id and change_id not in change_requests:
            return json.dumps({"error": f"Change request {change_id} not found", "halt": True})
        if problem_id and problem_id not in problem_tickets:
            return json.dumps({"error": f"Problem ticket {problem_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ["created", "assigned", "in_progress", "completed", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        workorder_id = str(generate_id(work_orders))
        timestamp = "2025-10-01T00:00:00"
        
        new_workorder = {
            "workorder_id": workorder_id,
            "incident_id": incident_id,
            "change_id": change_id,
            "problem_id": problem_id,
            "title": title,
            "work_type": work_type,
            "status": status,
            "assigned_to_user": assigned_to_user,
            "created_by_user": created_by_user,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        work_orders[workorder_id] = new_workorder
        return json.dumps({"workorder_id": workorder_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_workorder",
                "description": "Create a new work order",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Work order title"},
                        "work_type": {"type": "string", "description": "Type of work"},
                        "created_by_user": {"type": "string", "description": "User creating the work order"},
                        "incident_id": {"type": "string", "description": "Related incident ID"},
                        "change_id": {"type": "string", "description": "Related change request ID"},
                        "problem_id": {"type": "string", "description": "Related problem ticket ID"},
                        "assigned_to_user": {"type": "string", "description": "Assigned user ID"},
                        "status": {"type": "string", "description": "Work order status (created/assigned/in_progress/completed/cancelled)"}
                    },
                    "required": ["title", "work_type", "created_by_user"]
                }
            }
        }
EOF

# Tool 18: update_workorder
cat > tools/update_workorder.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateWorkorder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], workorder_id: str, change_set: Dict[str, Any],
               status: Optional[str] = None, assigned_to_user: Optional[str] = None) -> str:
        
        work_orders = data.get("work_orders", {})
        users = data.get("users", {})
        
        # Validate workorder exists
        if workorder_id not in work_orders:
            return json.dumps({"error": f"Work order {workorder_id} not found", "halt": True})
        
        # Update change_set with optional parameters if provided
        if status:
            change_set["status"] = status
        if assigned_to_user:
            change_set["assigned_to_user"] = assigned_to_user
        
        # Validate status if being updated
        if "status" in change_set:
            valid_statuses = ["created", "assigned", "in_progress", "completed", "cancelled"]
            if change_set["status"] not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate assigned user if being updated
        if "assigned_to_user" in change_set and change_set["assigned_to_user"]:
            if change_set["assigned_to_user"] not in users:
                return json.dumps({"error": f"Assigned user {change_set['assigned_to_user']} not found", "halt": True})
        
        # Apply changes
        for key, value in change_set.items():
            work_orders[workorder_id][key] = value
        
        work_orders[workorder_id]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(work_orders[workorder_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_workorder",
                "description": "Update a work order",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "workorder_id": {"type": "string", "description": "ID of the work order to update"},
                        "change_set": {"type": "object", "description": "Dictionary of changes to apply"},
                        "status": {"type": "string", "description": "New status (created/assigned/in_progress/completed/cancelled)"},
                        "assigned_to_user": {"type": "string", "description": "New assigned user"}
                    },
                    "required": ["workorder_id", "change_set"]
                }
            }
        }
EOF

# Tool 19: record_communication
cat > tools/record_communication.py << 'EOF'
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
EOF

# Tool 20: record_workaround
cat > tools/record_workaround.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class RecordWorkaround(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, implemented_by_user: str,
               effectiveness_level: str, implemented_at: str,
               status: Optional[str] = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        workarounds = data.get("workarounds", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if str(implemented_by_user) not in users:
            return json.dumps({"error": f"User {implemented_by_user} not found", "halt": True})
        
        # Validate effectiveness_level
        valid_levels = ["full_mitigation", "partial_mitigation", "minimal_impact"]
        if effectiveness_level not in valid_levels:
            return json.dumps({"error": f"Invalid effectiveness_level. Must be one of {valid_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["active", "inactive", "replaced"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        workaround_id = generate_id(workarounds)
        timestamp = "2025-10-01T00:00:00"
        
        new_workaround = {
            "workaround_id": workaround_id,
            "incident_id": incident_id,
            "implemented_by_user": implemented_by_user,
            "effectiveness_level": effectiveness_level,
            "status": status,
            "implemented_at": implemented_at,
            "created_at": timestamp
        }
        
        workarounds[workaround_id] = new_workaround
        return json.dumps({"workaround_id": workaround_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_workaround",
                "description": "Record a workaround for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "implemented_by_user": {"type": "string", "description": "User implementing workaround"},
                        "effectiveness_level": {"type": "string", "description": "Effectiveness level (full_mitigation, partial_mitigation, minimal_impact)"},
                        "implemented_at": {"type": "string", "description": "When workaround was implemented"},
                        "status": {"type": "string", "description": "Workaround status (active, inactive, replaced), defaults to active"}
                    },
                    "required": ["incident_id", "implemented_by_user", "effectiveness_level", "implemented_at"]
                }
            }
        }
EOF

# Tool 21: conduct_rca
cat > tools/conduct_rca.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ConductRca(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, conducted_by_user: str,
               analysis_method: str, status: Optional[str] = 'in_progress',
               completed_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        root_cause_analysis = data.get("root_cause_analysis", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate user exists
        if str(conducted_by_user) not in users:
            return json.dumps({"error": f"User {conducted_by_user} not found", "halt": True})
        
        # Validate analysis_method
        valid_methods = ["five_whys", "fishbone_diagram", "fault_tree_analysis", "timeline_analysis"]
        if analysis_method not in valid_methods:
            return json.dumps({"error": f"Invalid analysis_method. Must be one of {valid_methods}", "halt": True})
        
        # Validate status
        valid_statuses = ["in_progress", "completed", "reviewed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        analysis_id = generate_id(root_cause_analysis)
        timestamp = "2025-10-01T00:00:00"
        
        new_analysis = {
            "analysis_id": analysis_id,
            "incident_id": incident_id,
            "conducted_by_user": conducted_by_user,
            "analysis_method": analysis_method,
            "status": status,
            "completed_at": completed_at,
            "created_at": timestamp
        }
        
        root_cause_analysis[analysis_id] = new_analysis
        return json.dumps({"analysis_id": analysis_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "conduct_rca",
                "description": "Conduct root cause analysis for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "conducted_by_user": {"type": "string", "description": "User conducting RCA"},
                        "analysis_method": {"type": "string", "description": "Method of analysis (five_whys, fishbone_diagram, fault_tree_analysis, timeline_analysis)"},
                        "status": {"type": "string", "description": "RCA status (in_progress, completed, reviewed), defaults to in_progress"},
                        "completed_at": {"type": "string", "description": "When RCA was completed"}
                    },
                    "required": ["incident_id", "conducted_by_user", "analysis_method"]
                }
            }
        }
EOF

# Tool 22: submit_change_request
cat > tools/submit_change_request.py << 'EOF'
import json
from typing import Any, Dict, Optional

class SubmitChangeRequest:
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, change_type: str, risk_level: str,
               requesting_user: str, incident_id: Optional[str] = None, 
               status: Optional[str] = 'requested', approved_by_user: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        change_requests = data.get("change_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        
        # Validate requesting user exists
        if str(requesting_user) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user} not found", "halt": True})
        
        # Validate approved_by user if provided
        if approved_by_user and str(approved_by_user) not in users:
            return json.dumps({"error": f"Approving user {approved_by_user} not found", "halt": True})
        
        # Validate incident if provided
        if incident_id and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate change_type
        valid_change_types = ["normal", "standard", "upgrade", "emergency"]
        if change_type not in valid_change_types:
            return json.dumps({"error": f"Invalid change_type. Must be one of {valid_change_types}", "halt": True})
        
        # Validate risk_level
        valid_risk_levels = ["low", "medium", "high"]
        if risk_level not in valid_risk_levels:
            return json.dumps({"error": f"Invalid risk_level. Must be one of {valid_risk_levels}", "halt": True})
        
        # Validate status
        valid_statuses = ["requested", "in_progress", "scheduled", "rolled_back", "completed", "failed", "approved"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        change_id = generate_id(change_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_change_request = {
            "change_id": change_id,
            "incident_id": incident_id,
            "title": title,
            "change_type": change_type,
            "risk_level": risk_level,
            "status": status,
            "requesting_user": requesting_user,
            "approved_by_user": approved_by_user,
            "scheduled_start_time": None,
            "scheduled_end_time": None,
            "actual_start_time": None,
            "actual_end_time": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        change_requests[change_id] = new_change_request
        return json.dumps({"change_id": change_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_change_request",
                "description": "Submit a new change request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Change request title"},
                        "change_type": {"type": "string", "description": "Type of change (normal, standard, upgrade, emergency)"},
                        "risk_level": {"type": "string", "description": "Risk level of the change (low, medium, high)"},
                        "requesting_user": {"type": "string", "description": "User requesting the change"},
                        "incident_id": {"type": "string", "description": "Related incident ID if applicable"},
                        "status": {"type": "string", "description": "Change request status (requested, in_progress, scheduled, rolled_back, completed, failed, approved), defaults to 'requested'"},
                        "approved_by_user": {"type": "string", "description": "User who approved the change"}
                    },
                    "required": ["title", "change_type", "risk_level", "requesting_user"]
                }
            }
        }
EOF

# Tool 23: create_rollback_request
cat > tools/create_rollback_request.py << 'EOF'
import json
from typing import Any, Dict, Optional

class CreateRollbackRequest:
    @staticmethod
    def invoke(data: Dict[str, Any], change_id: str, requesting_user: str,
               incident_id: Optional[str] = None, status: Optional[str] = 'requested',
               approved_by_user: Optional[str] = None, completed_at: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        rollback_requests = data.get("rollback_requests", {})
        change_requests = data.get("change_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        
        # Validate change request exists
        if str(change_id) not in change_requests:
            return json.dumps({"error": f"Change request {change_id} not found", "halt": True})
        
        # Validate requesting user exists
        if str(requesting_user) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user} not found", "halt": True})
        
        # Validate approved_by user if provided
        if approved_by_user and str(approved_by_user) not in users:
            return json.dumps({"error": f"Approving user {approved_by_user} not found", "halt": True})
        
        # Validate incident if provided
        if incident_id and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ["requested", "in_progress", "failed", "approved"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        rollback_id = generate_id(rollback_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_rollback = {
            "rollback_id": rollback_id,
            "change_id": change_id,
            "incident_id": incident_id,
            "requesting_user": requesting_user,
            "status": status,
            "approved_by_user": approved_by_user,
            "completed_at": completed_at,
            "created_at": timestamp
        }
        
        rollback_requests[rollback_id] = new_rollback
        return json.dumps({"rollback_id": rollback_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_rollback_request",
                "description": "Create a rollback request for a change",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "change_id": {"type": "string", "description": "ID of the change to rollback"},
                        "requesting_user": {"type": "string", "description": "User requesting rollback"},
                        "incident_id": {"type": "string", "description": "Related incident ID if applicable"},
                        "status": {"type": "string", "description": "Rollback status (requested, in_progress, failed, approved), defaults to 'requested'"},
                        "approved_by_user": {"type": "string", "description": "User who approved the rollback"},
                        "completed_at": {"type": "string", "description": "When rollback was completed (YYYY-MM-DD)"}
                    },
                    "required": ["change_id", "requesting_user"]
                }
            }
        }
EOF

# Tool 24: log_metric
cat > tools/log_metric.py << 'EOF'
import json
from typing import Any, Dict, Optional

class LogMetric:
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
                "name": "log_metric",
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
EOF

# Tool 25: generate_incident_report
cat > tools/generate_incident_report.py << 'EOF'
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
EOF

# Tool 26: record_kb_article
cat > tools/record_kb_article.py << 'EOF'
import json
from typing import Any, Dict, Optional

class RecordKbArticle:
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
                "name": "record_kb_article",
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
EOF

# Tool 27: submit_post_incident_review
cat > tools/submit_post_incident_review.py << 'EOF'
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
EOF

# Tool 28: log_audit
cat > tools/log_audit.py << 'EOF'
import json
from typing import Any, Dict

class LogAudit:
    @staticmethod
    def invoke(data: Dict[str, Any], action_type: str, entity_type: str,
               entity_id: str, performed_by_user: str, action_details: Dict[str, Any],
               timestamp: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        audit_logs = data.get("audit_logs", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(performed_by_user) not in users:
            return json.dumps({"error": f"User {performed_by_user} not found", "halt": True})
        
        audit_id = generate_id(audit_logs)
        
        new_audit = {
            "audit_id": audit_id,
            "action": action_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "audit_by_user": performed_by_user,
            "created_at": timestamp
        }
        
        # Store action details separately if needed
        audit_logs[audit_id] = new_audit
        
        return json.dumps({"audit_id": audit_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit",
                "description": "Log an audit entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_type": {"type": "string", "description": "Type of action being audited"},
                        "entity_type": {"type": "string", "description": "Type of entity affected"},
                        "entity_id": {"type": "string", "description": "ID of the entity"},
                        "performed_by_user": {"type": "string", "description": "User performing the action"},
                        "action_details": {"type": "object", "description": "Details of the action"},
                        "timestamp": {"type": "string", "description": "When action was performed (YYYY-MM-DD)"}
                    },
                    "required": ["action_type", "entity_type", "entity_id", "performed_by_user", "action_details", "timestamp"]
                }
            }
        }
EOF

# Tool 29: discover_client
cat > tools/discover_client.py << 'EOF'
import json
from typing import Any, Dict, Optional

class DiscoverClient:
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
                "name": "discover_client",
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
EOF

# Tool 30: discover_user
cat > tools/discover_user.py << 'EOF'
import json
from typing import Any, Dict, Optional

class DiscoverUser:
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               email: Optional[str] = None, role: Optional[str] = None,
               client_id: Optional[str] = None, vendor_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if user_id and str(user.get("user_id")) != str(user_id):
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if role and user.get("role") != role:
                continue
            if client_id and user.get("client_id") != client_id:
                continue
            if vendor_id and user.get("vendor_id") != vendor_id:
                continue
            if status and user.get("status") != status:
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_user",
                "description": "Discover users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by email address"},
                        "role": {"type": "string", "description": "Filter by role (system_administrator, incident_manager, technical_support, account_manager, executive, client_contact, vendor_contact)"},
                        "client_id": {"type": "string", "description": "Filter by associated client"},
                        "vendor_id": {"type": "string", "description": "Filter by associated vendor"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, on_leave)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 31: discover_vendor
cat > tools/discover_vendor.py << 'EOF'
import json
from typing import Any, Dict, Optional

class DiscoverVendor:
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_id: Optional[str] = None,
               vendor_name: Optional[str] = None, vendor_email: Optional[str] = None,
               vendor_phone: Optional[str] = None, vendor_type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        vendors = data.get("vendors", {})
        results = []
        
        for vendor in vendors.values():
            if vendor_id and str(vendor.get("vendor_id")) != str(vendor_id):
                continue
            if vendor_name and vendor_name.lower() not in vendor.get("vendor_name", "").lower():
                continue
            if vendor_email and vendor.get("contact_email", "").lower() != vendor_email.lower():
                continue
            if vendor_phone and vendor.get("contact_phone") != vendor_phone:
                continue
            if vendor_type and vendor.get("vendor_type") != vendor_type:
                continue
            if status and vendor.get("status") != status:
                continue
            results.append(vendor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_vendor",
                "description": "Discover vendors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "Filter by vendor ID"},
                        "vendor_name": {"type": "string", "description": "Filter by vendor name (partial match)"},
                        "vendor_email": {"type": "string", "description": "Filter by email"},
                        "vendor_phone": {"type": "string", "description": "Filter by phone"},
                        "vendor_type": {"type": "string", "description": "Filter by vendor type (technology_provider, infrastructure_provider, security_provider, consulting_services, maintenance_services, cloud_provider, payment_processor)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 32: discover_product
cat > tools/discover_product.py << 'EOF'
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
EOF

# Tool 33: discover_component
cat > tools/discover_component.py << 'EOF'
import json
from typing import Any, Dict, Optional

class DiscoverComponent:
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
                "name": "discover_component",
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
EOF

# Tool 34: discover_incident
cat > tools/discover_incident.py << 'EOF'
import json
from typing import Any, Dict, Optional

class DiscoverIncident:
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               client_id: Optional[str] = None, severity: Optional[str] = None,
               status: Optional[str] = None, assigned_to_user_id: Optional[str] = None,
               reporter_user_id: Optional[str] = None) -> str:
        
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if incident_id and str(incident.get("incident_id")) != str(incident_id):
                continue
            if client_id and incident.get("client_id") != client_id:
                continue
            if severity and incident.get("severity") != severity:
                continue
            if status and incident.get("status") != status:
                continue
            if assigned_to_user_id and incident.get("assigned_to_user_id") != assigned_to_user_id:
                continue
            if reporter_user_id and incident.get("reporter_user_id") != reporter_user_id:
                continue
            results.append(incident)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_incident",
                "description": "Discover incidents with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "client_id": {"type": "string", "description": "Filter by client"},
                        "severity": {"type": "string", "description": "Filter by severity (P1, P2, P3, P4)"},
                        "status": {"type": "string", "description": "Filter by status (open, investigating, in_progress, resolved, closed)"},
                        "assigned_to_user_id": {"type": "string", "description": "Filter by assignee"},
                        "reporter_user_id": {"type": "string", "description": "Filter by reporter"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 35: discover_subscription
cat > tools/discover_subscription.py << 'EOF'
import json
from typing import Any, Dict, Optional

class DiscoverSubscription:
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: Optional[str] = None,
               client_id: Optional[str] = None, product_id: Optional[str] = None,
               sla_tier: Optional[str] = None, status: Optional[str] = None) -> str:
        
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if subscription_id and str(subscription.get("subscription_id")) != str(subscription_id):
                continue
            if client_id and subscription.get("client_id") != client_id:
                continue
            if product_id and subscription.get("product_id") != product_id:
                continue
            if sla_tier and subscription.get("sla_tier") != sla_tier:
                continue
            if status and subscription.get("status") != status:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_subscription",
                "description": "Discover subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "client_id": {"type": "string", "description": "Filter by client"},
                        "product_id": {"type": "string", "description": "Filter by product"},
                        "sla_tier": {"type": "string", "description": "Filter by SLA tier (basic, standard, premium)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, cancelled, expired)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 36: transfer_to_human
cat > tools/transfer_to_human.py << 'EOF'
import json
from typing import Any, Dict

class TransferToHuman:
    @staticmethod
    def invoke(data: Dict[str, Any], reason: str, context: Dict[str, Any],
               escalation_level: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        transfers = data.get("human_transfers", {})
        
        # Validate escalation_level
        valid_levels = ["management", "technical", "executive", "vendor"]
        if escalation_level not in valid_levels:
            return json.dumps({"error": f"Invalid escalation_level. Must be one of {valid_levels}", "halt": True})
        
        transfer_id = generate_id(transfers)
        timestamp = "2025-10-01T00:00:00"
        
        new_transfer = {
            "transfer_id": transfer_id,
            "reason": reason,
            "context": context,
            "escalation_level": escalation_level,
            "created_at": timestamp
        }
        
        transfers[transfer_id] = new_transfer
        return json.dumps({"transfer_id": transfer_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_to_human",
                "description": "Transfer the conversation to a human agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {"type": "string", "description": "Reason for transfer"},
                        "context": {"type": "object", "description": "Context information for the transfer"},
                        "escalation_level": {"type": "string", "description": "Level of escalation needed (management, technical, executive, vendor)"}
                    },
                    "required": ["reason", "context", "escalation_level"]
                }
            }
        }
EOF

echo "All tool files have been created successfully!"