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

### Client Management

**Authorized user role:** System Administrator, Account Manager (assigned to the client for update operation)

**1\. Client Onboarding**

Onboard a new client (enterprise, mid-market, small business, or startup) in the incident management system to enable incident tracking and service subscriptions.

Inputs:

- Required: client_name, registration_number (unique), contact_email (unique), client_type
- Optional: country, industry, status (default: 'active')

Steps:

- Verify that registration_number and contact_email are unique.
- Collect all required client information from the user.
- Create the client record using create_client.
- Default status = active unless specified by user; return client_id.
- Create an audit entry for client creation using log_audit.

Halt conditions: Missing or invalid inputs; duplicate registration number or email; unauthorized user; creation failed

**2\. Client Information Update**

Modify existing client details or update the client's status to keep records accurate and aligned with current business needs.

Inputs:

- Obtain client_id
- change_set (such as status modification or other client details)

Steps:

- Check uniqueness for registration_number and contact_email if being updated.
- Retrieve current client record.
- Update the requested changes using update_client with the current timestamp.
- Create an audit entry for the update using log_audit.

Halt conditions: Client not found; duplicate registration_number or contact_email; unauthorized user; update failed

### User Management

**Authorized user roles:** System Administrator, Incident Manager

**1\. Register User Account**

Add personnel to the incident management system with proper role, client/vendor association, and active status.

Inputs:

- Required: name, email (unique), role
- Optional: department, client_id, vendor_id, timezone (default: 'UTC'), status (default: 'active')

Steps:

- Check that the email address is unique.
- Confirm that specified client_id or vendor_id exists if association is provided.
- Create the user record with active status using register_user.
- Create an audit entry for the user creation using log_audit.

Halt conditions: Missing required fields; duplicate email; specified client/vendor does not exist;

creation failed

**2\. Update User Details**

Modify existing user role assignments, or status while ensuring authorization.

Inputs:

- Obtain user_id
- change_set (such as status modification or role assignments)

Steps:

- Verify that the user record exists.
- Validate that the new role assignment exists in the allowed enumeration.
- Update the requested changes using update_user with the current timestamp.
- Create an audit entry for the update using log_audit.

Halt conditions: User record not found; unauthorized request; invalid role assignment; update failed

### Vendor Management

**Authorized user role:** System administrators, incident managers, and executives.

**Register Vendor Information**

Add external service providers to the incident management system, ensuring uniqueness and proper classification.

Inputs:

- Required: vendor_name (unique), vendor_email (unique), vendor_phone (unique), vendor_type
- Optional: status (default: 'active')

Steps:

- Check that vendor_name, contact_email, and contact_phone are unique.
- Confirm that vendor_type exists in the allowed enumeration.
- Create (create_vendor) the vendor record with active status unless otherwise specified.
- Create an audit entry for vendor registration using log_audit.

Halt conditions: Missing required fields; duplicate vendor name, email, or phone; invalid vendor_type; creation failed

## Authority and Access Controls

**Permission Validation**

All operations enforce user authority based on:

- Role: incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact
- Client association: user must be linked to the relevant client_id
- Vendor association: user must be linked to the relevant vendor_id
- Active status: user must be active in the users table
