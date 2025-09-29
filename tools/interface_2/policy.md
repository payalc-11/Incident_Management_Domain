# Incident Management Policy (Client, User & Vendor Management)
The current time is 2025-09-25 12:00:00 UTC

## Common Standards (applies to all SOPs)
- Validation: Halt with a clear error if required inputs are missing or invalid.  
- Authorization & Approvals: Enforce role-based access. Approvers can act without self-signoff unless SOP mandates another role.  
- Logging & Audit: Log every create/update/approve/reject/delete/execute.  
- Halt Conditions: Stop with clear messaging (and escalate if needed) when inputs, approvals, or external calls fail.  
- Data Minimization: Store only necessary audit context; avoid raw PII or full datasets.  
- Tool Usage: Use only provided tools—no invented steps or integrations.  

## Roles and Responsibilities

#### System Administrator

- Manage clients, users, vendors, and products; configure system settings; maintain infrastructure components; manage permissions and subscriptions.

#### Incident Manager

- Oversee incidents through lifecycle; coordinate escalations and communications; approve SLAs and subscriptions; facilitate post-incident reviews and root cause analysis.

#### Technical Support

- Handle incident investigations; implement workarounds; conduct root cause analysis; maintain knowledge base; manage infrastructure components and technical changes.

#### Account Manager

- Maintain client records and subscriptions; define service levels; manage client relationships; coordinate incident communications.

#### Executive

- Approve high-level policies and escalations; manage critical subscriptions and vendor agreements; authorize major changes and resources.

#### Vendor Contact

- Report and update on incidents; coordinate with internal teams for vendor-related issues.

#### Client Contact

- Report incidents affecting their organization; receive updates and manage internal communications during incidents. 

## Standard Operating Procedures (SOPs)

### Product and Infrastructure

**Authorized user role:** Technical support, system administrators

**1\. Adding Product**

Add new systems, applications, or services to the incident management system for tracking and coverage.

Inputs:

- Required: product_name (unique), product_type
- Optional: version, support_vendor_id

Steps:

- Check that the product_name is unique.
- Confirm supplier_vendor_id exists if linking to an external vendor.
- Create the product record with the current timestamp using add_product.
- Create an audit entry for product registration using log_audit.

Halt conditions: Missing required fields; duplicate product name; vendor does not exist; creation failed

**2\. Adding Infrastructure Component**

Document system components supporting products and services, including operational and environment details.

Inputs:

- Required: component_name (unique), component_type, environment
- Optional: product_id, location, port_number, operational_status (default: 'operational')

Steps:

- Check that component_name is unique within the associated product.
- Confirm product_id exists if the component is linked to a product.
- Create the infrastructure component record using add_component.
- Create an audit entry for component registration using audit_log.

Halt conditions: Missing required fields; duplicate component name under same product; invalid product_id; creation failed

### Subscription and Service Level Management

**1\. Creating Client Subscriptions**

Establish service agreements and coverage levels for clients.

**Authorized user role:** Account managers, incident manager, executive

Inputs:

- Required: client_id, product_id, subscription_type, sla_tier, start_date, end_date
- Optional: rto_hours, status (default: 'active')

Steps:

- Verify that the client and product record exists.
- Link the subscription to the client and product records.
- Set recovery time objectives (if specified).
- Confirm all required fields are provided.
- Create the subscription record with 'active' status using create_client_subscription.
- Log an audit entry for subscription creation.

Halt conditions: Missing required fields; client or product record does not exist; invalid dates; creation failed

**2\. Creating SLA agreement**

Define specific SLA metrics for client subscriptions.

**Authorized user role:** Account managers, system administrators, executives

Inputs:

- Required: subscription_id, response_time_minutes, resolution_time_hours
- Optional: availability_percentage

Steps:

- Verify subscription exists and is active.
- Check user has authority to create SLA agreements for the client.
- Validate response/resolution times align with the subscription tier.
- Create SLA record linked to subscription using create_sla_record and return sla_id.
- Log an audit entry for SLA creation.

Halt conditions: Subscription not active; invalid user authority; invalid SLA parameters; creation failed

**3\. Managing Service Level Agreements (SLAs)**

Define response and resolution requirements for different incident severities.

**Authorized user role:** Account managers, incident manager, executive

Inputs:

- Required: subscription_id, severity_level, response_time_minutes, resolution_time_hours
- Optional: availability_percentage

Steps:

- Verify that the subscription record exists.
- Check that the severity level exists in the allowed enumeration.
- Confirm all required fields are provided.
- Create the SLA record linked to the subscription using manage_sla_record.
- Log an audit entry for SLA creation.

Halt conditions: Missing required fields; subscription record not found; invalid severity level; creation failed

## Authority and Access Controls

**Permission Validation**

All operations enforce user authority based on:

- Role: incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact
- Client association: user must be linked to the relevant client_id
- Vendor association: user must be linked to the relevant vendor_id
- Active status: user must be active in the users table
