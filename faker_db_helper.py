import json
import random
from datetime import datetime, timedelta
from faker import Faker
from typing import Dict, List, Any, Optional
import os

fake = Faker()
Faker.seed(42)  # For reproducible results
random.seed(42)

# Constants for realistic data generation
EMAIL_DOMAINS = ['gmail.com', 'outlook.com', 'company.com', 'corporate.net', 'enterprise.org', 'tech.io']
AREA_CODES = ['415', '212', '310', '312', '202', '404', '503', '206', '617', '713']

# Enum values from schema
CLIENT_TYPES = ['enterprise', 'mid_market', 'small_business', 'startup']
USER_ROLES = ['system_administrator', 'incident_manager', 'technical_support', 
              'account_manager', 'executive', 'client_contact', 'vendor_contact']
USER_STATUSES = ['active', 'inactive', 'on_leave']
VENDOR_TYPES = ['technology_provider', 'infrastructure_provider', 'security_provider',
                'consulting_services', 'maintenance_services', 'cloud_provider', 'payment_processor']
PRODUCT_STATUSES = ['active', 'deprecated', 'maintenance', 'end_of_life']
ENVIRONMENTS = ['production', 'staging', 'development', 'testing']
COMP_STATUSES = ['operational', 'degraded', 'offline', 'maintenance']
SUBSCRIPTION_TYPES = ['trial', 'limited_service', 'full_service', 'custom']
SLA_TIERS = ['basic', 'standard', 'premium']
SUBS_STATUSES = ['active', 'inactive', 'cancelled', 'expired']
SEVERITY_LEVELS = ['P1', 'P2', 'P3', 'P4']
IMPACT_LEVELS = ['low', 'medium', 'high', 'critical']
INCIDENT_STATUSES = ['open', 'investigating', 'in_progress', 'resolved', 'closed']
ESC_LEVELS = ['management', 'technical', 'executive', 'vendor']
ESC_STATUSES = ['active', 'resolved', 'cancelled']
RECEIVER_TYPES = ['client_contacts', 'executive_team', 'technical_team', 'all_stakeholders']
DELIVERY_METHODS = ['email', 'sms', 'phone', 'chat', 'dashboard_notification']
DELIVERY_STATUSES = ['pending', 'sent', 'delivered', 'failed']
EFFECTIVENESS_LEVELS = ['full_mitigation', 'partial_mitigation', 'minimal_impact']
WORKAROUND_STATUSES = ['active', 'inactive', 'replaced']
RCA_METHODS = ['five_whys', 'fishbone_diagram', 'fault_tree_analysis', 'timeline_analysis']
RCA_STATUSES = ['in_progress', 'completed', 'reviewed']
CHANGE_TYPES = ['normal', 'standard', 'upgrade', 'emergency']
RISK_LEVELS = ['low', 'medium', 'high']
CHANGE_STATUSES = ['requested', 'in_progress', 'scheduled', 'rolled_back', 'completed', 'failed', 'approved']
ROLLBACK_STATUSES = ['requested', 'in_progress', 'failed', 'approved']
METRIC_TYPES = ['response_time', 'resolution_time', 'detection_time', 'escalation_time']
REPORT_TYPES = ['executive_summary', 'compliance_report', 'technical_details', 'business_impact', 'post_mortem']
REPORT_STATUSES = ['completed', 'draft', 'published']
KBA_TYPES = ['troubleshooting', 'resolution_procedure', 'prevention_guide', 'faq']
KBA_CATEGORIES = ['technical', 'process', 'communication', 'escalation']
KBA_STATUSES = ['draft', 'under_review', 'archived', 'published']
REVIEW_RATINGS = ['excellent', 'good', 'satisfactory', 'needs_improvement', 'poor']
REVIEW_STATUSES = ['scheduled', 'completed', 'cancelled']
WORKORDER_STATUSES = ['created', 'assigned', 'in_progress', 'completed', 'cancelled']

# Industry names for clients
INDUSTRIES = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing', 
              'Education', 'Government', 'Telecommunications', 'Energy', 'Transportation']

# Product types and names
PRODUCT_TYPES = ['Software', 'Platform', 'Service', 'Infrastructure', 'Security', 'Database']
PRODUCT_NAMES = ['CloudSync', 'DataFlow', 'SecureNet', 'AppManager', 'ServerMonitor', 
                 'LoadBalancer', 'APIGateway', 'CacheService', 'QueueManager', 'AuthService']

# Component types
COMPONENT_TYPES = ['Server', 'Database', 'Network', 'Storage', 'Application', 'Service', 'API', 'Cache']

# Incident categories
INCIDENT_CATEGORIES = ['Performance', 'Connectivity', 'Security', 'Data', 'Access', 'Configuration', 'Hardware']

def generate_email(first_name: str, last_name: str) -> str:
    """Generate realistic email addresses"""
    domain = random.choice(EMAIL_DOMAINS)
    rand_num = random.randint(1, 999)
    formats = [
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name.lower()}{last_name.lower()}{rand_num}@{domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{domain}",
        f"{first_name.lower()}{rand_num}@{domain}"
    ]
    return random.choice(formats)

def generate_phone() -> str:
    """Generate realistic phone numbers"""
    area_code = random.choice(AREA_CODES)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"+1{area_code}{exchange}{number}"

def generate_timestamps(base_date: Optional[datetime] = None) -> tuple:
    """Generate created_at and updated_at timestamps"""
    if base_date is None:
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
    else:
        created_at = base_date
    
    # updated_at should be after created_at
    days_diff = random.randint(0, 90)
    updated_at = created_at + timedelta(days=days_diff, hours=random.randint(0, 23))
    
    return created_at.isoformat(), updated_at.isoformat()

class IncidentManagementSeeder:
    def __init__(self):
        self.data = {}
        self.id_counter = {}
        
    def get_next_id(self, table_name: str) -> str:
        """Get next incremental ID for a table"""
        if table_name not in self.id_counter:
            self.id_counter[table_name] = 1
        else:
            self.id_counter[table_name] += 1
        return str(self.id_counter[table_name])
    
    def generate_clients(self, count: int = 15) -> Dict[str, Any]:
        """Generate client records"""
        clients = {}
        for _ in range(count):
            client_id = self.get_next_id('clients')
            created_at, updated_at = generate_timestamps()
            
            company_name = fake.company()
            
            clients[client_id] = {
                'client_id': str(client_id),
                'client_name': company_name,
                'registration_number': f"REG{fake.random_number(digits=8)}",
                'contact_email': f"contact@{company_name.lower().replace(' ', '').replace(',', '')}{''.join(random.choice('.com.net.org'.split('.')) for _ in range(1))}",
                'client_type': random.choice(CLIENT_TYPES),
                'industry': random.choice(INDUSTRIES),
                'country': fake.country(),
                'status': random.choices(['active', 'inactive', 'suspended'], weights=[0.8, 0.15, 0.05])[0],
                'created_at': created_at,
                'updated_at': updated_at
            }
        return clients
    
    def generate_vendors(self, count: int = 10) -> Dict[str, Any]:
        """Generate vendor records"""
        vendors = {}
        used_emails = set()
        used_phones = set()
        
        for _ in range(count):
            vendor_id = self.get_next_id('vendors')
            vendor_name = f"{fake.company()} {random.choice(['Technologies', 'Solutions', 'Services', 'Systems'])}"
            
            # Generate unique email
            email = f"vendor@{vendor_name.lower().replace(' ', '')}.com"
            while email in used_emails:
                email = f"vendor{random.randint(1, 999)}@{vendor_name.lower().replace(' ', '')}.com"
            used_emails.add(email)
            
            # Generate unique phone
            phone = generate_phone()
            while phone in used_phones:
                phone = generate_phone()
            used_phones.add(phone)
            
            vendors[vendor_id] = {
                'vendor_id': str(vendor_id),
                'vendor_name': vendor_name,
                'vendor_type': random.choice(VENDOR_TYPES),
                'contact_email': email,
                'contact_phone': phone,
                'status': random.choices(['active', 'inactive'], weights=[0.9, 0.1])[0],
                'created_at': fake.date_time_between(start_date='-2y', end_date='now').isoformat()
            }
        return vendors
    
    def generate_users(self, clients: Dict, vendors: Dict, count: int = 50) -> Dict[str, Any]:
        """Generate user records"""
        users = {}
        used_emails = set()
        
        client_ids = list(clients.keys())
        vendor_ids = list(vendors.keys())
        
        for _ in range(count):
            user_id = self.get_next_id('users')
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            # Generate unique email
            email = generate_email(first_name, last_name)
            while email in used_emails:
                email = generate_email(first_name, last_name)
            used_emails.add(email)
            
            role = random.choice(USER_ROLES)
            created_at, updated_at = generate_timestamps()
            
            user_data = {
                'user_id': str(user_id),
                'name': f"{first_name} {last_name}",
                'email': email,
                'role': role,
                'department': random.choice(['IT', 'Operations', 'Support', 'Management', 'Engineering']),
                'client_id': None,
                'vendor_id': None,
                'timezone': random.choice(['UTC', 'EST', 'PST', 'CST', 'GMT', 'CET']),
                'status': random.choice(USER_STATUSES),
                'created_at': created_at,
                'updated_at': updated_at
            }
            
            # Assign client_id only for client_contact role
            if role == 'client_contact' and client_ids:
                user_data['client_id'] = str(random.choice(client_ids))
            
            # Assign vendor_id only for vendor_contact role
            elif role == 'vendor_contact' and vendor_ids:
                user_data['vendor_id'] = str(random.choice(vendor_ids))
            
            users[user_id] = user_data
        
        return users
    
    def generate_products(self, vendors: Dict, count: int = 20) -> Dict[str, Any]:
        """Generate product records"""
        products = {}
        vendor_ids = list(vendors.keys())
        used_names = set()
        
        for _ in range(count):
            product_id = self.get_next_id('products')
            
            # Generate unique product name
            product_name = f"{random.choice(PRODUCT_NAMES)} {random.choice(['Pro', 'Enterprise', 'Basic', 'Plus', ''])}"
            while product_name in used_names:
                product_name = f"{random.choice(PRODUCT_NAMES)} {random.choice(['Pro', 'Enterprise', 'Basic', 'Plus', 'v2'])}"
            used_names.add(product_name)
            
            created_at, updated_at = generate_timestamps()
            
            products[product_id] = {
                'product_id': str(product_id),
                'product_name': product_name.strip(),
                'product_type': random.choice(PRODUCT_TYPES),
                'version': f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 99)}",
                'support_vendor_id': str(random.choice(vendor_ids)) if vendor_ids and random.random() > 0.3 else None,
                'status': random.choice(PRODUCT_STATUSES),
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return products
    
    def generate_infrastructure_components(self, products: Dict, count: int = 30) -> Dict[str, Any]:
        """Generate infrastructure component records"""
        components = {}
        product_ids = list(products.keys())
        used_names = set()
        
        for _ in range(count):
            component_id = self.get_next_id('components')
            
            # Generate unique component name
            comp_type = random.choice(COMPONENT_TYPES)
            comp_name = f"{comp_type}-{random.choice(['primary', 'secondary', 'backup', 'main', 'replica'])}-{random.randint(1, 99)}"
            while comp_name in used_names:
                comp_name = f"{comp_type}-{random.choice(['primary', 'secondary', 'backup', 'main', 'replica'])}-{random.randint(1, 999)}"
            used_names.add(comp_name)
            
            created_at, updated_at = generate_timestamps()
            
            components[component_id] = {
                'component_id': str(component_id),
                'component_name': comp_name,
                'component_type': comp_type,
                'product_id': str(random.choice(product_ids)) if product_ids and random.random() > 0.2 else None,
                'environment': random.choice(ENVIRONMENTS),
                'location': random.choice(['US-East', 'US-West', 'EU-Central', 'Asia-Pacific', 'UK-South']),
                'port_number': str(random.choice([80, 443, 3306, 5432, 6379, 8080, 9000, 27017])),
                'operational_status': random.choice(COMP_STATUSES),
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return components
    
    def generate_subscriptions(self, clients: Dict, products: Dict, count: int = 25) -> Dict[str, Any]:
        """Generate subscription records"""
        subscriptions = {}
        client_ids = list(clients.keys())
        product_ids = list(products.keys())
        
        for _ in range(count):
            subscription_id = self.get_next_id('subscriptions')
            
            start_date = fake.date_between(start_date='-2y', end_date='today')
            end_date = fake.date_between(start_date=start_date, end_date='+2y')
            created_at, updated_at = generate_timestamps()
            
            subscriptions[subscription_id] = {
                'subscription_id': str(subscription_id),
                'client_id': str(random.choice(client_ids)),
                'product_id': str(random.choice(product_ids)),
                'subscription_type': random.choice(SUBSCRIPTION_TYPES),
                'sla_tier': random.choice(SLA_TIERS),
                'rto_hours': random.choice([4, 8, 12, 24, 48, 72]),
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'status': random.choice(SUBS_STATUSES),
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return subscriptions
    
    def generate_slas(self, subscriptions: Dict) -> Dict[str, Any]:
        """Generate SLA records (1-3 per subscription)"""
        slas = {}
        
        for sub_id in subscriptions.keys():
            num_slas = random.randint(1, 3)
            for i in range(num_slas):
                sla_id = self.get_next_id('slas')
                
                severity = SEVERITY_LEVELS[i] if i < len(SEVERITY_LEVELS) else random.choice(SEVERITY_LEVELS)
                
                slas[sla_id] = {
                    'sla_id': str(sla_id),
                    'subscription_id': str(sub_id),
                    'severity_level': severity,
                    'response_time_minutes': random.choice([15, 30, 60, 120, 240]),
                    'resolution_time_hours': random.choice([2, 4, 8, 24, 48, 72]),
                    'availability_percentage': round(random.uniform(95.0, 99.9), 1),
                    'created_at': fake.date_time_between(start_date='-1y', end_date='now').isoformat()
                }
        
        return slas
    
    def generate_incidents(self, clients: Dict, components: Dict, users: Dict, count: int = 40) -> Dict[str, Any]:
        """Generate incident records"""
        incidents = {}
        client_ids = list(clients.keys())
        component_ids = list(components.keys())
        user_ids = list(users.keys())
        
        for _ in range(count):
            incident_id = self.get_next_id('incidents')
            
            detection_time = fake.date_time_between(start_date='-6m', end_date='now')
            created_at, updated_at = generate_timestamps(detection_time)
            
            status = random.choice(INCIDENT_STATUSES)
            resolution_time = None
            if status in ['resolved', 'closed']:
                resolution_time = (detection_time + timedelta(hours=random.randint(1, 72))).isoformat()
            
            incidents[incident_id] = {
                'incident_id': str(incident_id),
                'title': f"{random.choice(INCIDENT_CATEGORIES)} issue in {random.choice(['production', 'staging', 'development'])}",
                'category': random.choice(INCIDENT_CATEGORIES),
                'severity': random.choice(SEVERITY_LEVELS),
                'impact_level': random.choice(IMPACT_LEVELS),
                'urgency_level': random.choice(IMPACT_LEVELS),
                'status': status,
                'client_id': str(random.choice(client_ids)),
                'component_id': str(random.choice(component_ids)),
                'reporter_user_id': str(random.choice(user_ids)),
                'assigned_to_user_id': str(random.choice(user_ids)) if random.random() > 0.2 else None,
                'detection_timestamp': detection_time.isoformat(),
                'resolution_timestamp': resolution_time,
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return incidents
    
    def generate_incident_escalations(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate escalation records (0-2 per incident)"""
        escalations = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            num_escalations = random.choices([0, 1, 2], weights=[0.5, 0.35, 0.15])[0]
            
            for _ in range(num_escalations):
                escalation_id = self.get_next_id('escalations')
                
                escalated_at = fake.date_time_between(start_date='-3m', end_date='now')
                status = random.choice(ESC_STATUSES)
                resolved_at = None
                if status == 'resolved':
                    resolved_at = (escalated_at + timedelta(hours=random.randint(1, 48))).isoformat()
                
                escalations[escalation_id] = {
                    'escalation_id': str(escalation_id),
                    'incident_id': str(incident_id),
                    'escalated_by_user': str(random.choice(user_ids)),
                    'escalated_to_user': str(random.choice(user_ids)),
                    'escalation_level': random.choice(ESC_LEVELS),
                    'reason': f"Escalated due to {random.choice(['high priority', 'customer impact', 'technical complexity', 'resource requirements'])}",
                    'status': status,
                    'escalated_at': escalated_at.isoformat(),
                    'resolved_at': resolved_at,
                    'created_at': escalated_at.isoformat()
                }
        
        return escalations
    
    def generate_communications(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate communication records (1-3 per incident)"""
        communications = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            num_comms = random.randint(1, 3)
            
            for _ in range(num_comms):
                comm_id = self.get_next_id('communications')
                
                delivery_status = random.choice(DELIVERY_STATUSES)
                sent_at = None
                if delivery_status in ['sent', 'delivered', 'failed']:
                    sent_at = fake.date_time_between(start_date='-3m', end_date='now').isoformat()
                
                communications[comm_id] = {
                    'communication_id': str(comm_id),
                    'incident_id': str(incident_id),
                    'sender_id': str(random.choice(user_ids)),
                    'recipient_id': str(random.choice(user_ids)),
                    'recipient_type': random.choice(RECEIVER_TYPES) if random.random() > 0.7 else None,
                    'communication_type': random.choice(['update', 'notification', 'escalation', 'resolution']),
                    'delivery_method': random.choice(DELIVERY_METHODS),
                    'delivery_status': delivery_status,
                    'sent_at': sent_at,
                    'created_at': fake.date_time_between(start_date='-3m', end_date='now').isoformat()
                }
        
        return communications
    
    def generate_workarounds(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate workaround records (0-2 per incident)"""
        workarounds = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            num_workarounds = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1])[0]
            
            for _ in range(num_workarounds):
                workaround_id = self.get_next_id('workarounds')
                
                implemented_at = fake.date_time_between(start_date='-3m', end_date='now')
                
                workarounds[workaround_id] = {
                    'workaround_id': str(workaround_id),
                    'incident_id': str(incident_id),
                    'implemented_by_user': str(random.choice(user_ids)),
                    'effectiveness_level': random.choice(EFFECTIVENESS_LEVELS),
                    'status': random.choice(WORKAROUND_STATUSES),
                    'implemented_at': implemented_at.isoformat(),
                    'created_at': implemented_at.isoformat()
                }
        
        return workarounds
    
    def generate_root_cause_analyses(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate RCA records (0-1 per incident)"""
        rcas = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            if random.random() > 0.6:  # 40% chance of RCA
                rca_id = self.get_next_id('rcas')
                
                status = random.choice(RCA_STATUSES)
                completed_at = None
                if status in ['completed', 'reviewed']:
                    completed_at = fake.date_time_between(start_date='-2m', end_date='now').isoformat()
                
                rcas[rca_id] = {
                    'analysis_id': str(rca_id),
                    'incident_id': str(incident_id),
                    'conducted_by_user': str(random.choice(user_ids)),
                    'analysis_method': random.choice(RCA_METHODS),
                    'status': status,
                    'completed_at': completed_at,
                    'created_at': fake.date_time_between(start_date='-3m', end_date='now').isoformat()
                }
        
        return rcas
    
    def generate_change_requests(self, incidents: Dict, users: Dict, count: int = 30) -> Dict[str, Any]:
        """Generate change request records"""
        changes = {}
        incident_ids = list(incidents.keys())
        user_ids = list(users.keys())
        
        for _ in range(count):
            change_id = self.get_next_id('changes')
            
            status = random.choice(CHANGE_STATUSES)
            created_at, updated_at = generate_timestamps()
            
            scheduled_start = fake.date_time_between(start_date='now', end_date='+30d')
            scheduled_end = scheduled_start + timedelta(hours=random.randint(1, 8))
            
            actual_start = None
            actual_end = None
            if status in ['completed', 'failed', 'rolled_back']:
                actual_start = scheduled_start.isoformat()
                actual_end = (scheduled_start + timedelta(hours=random.randint(1, 12))).isoformat()
            
            changes[change_id] = {
                'change_id': str(change_id),
                'incident_id': str(random.choice(incident_ids)) if random.random() > 0.4 else None,
                'title': f"{random.choice(CHANGE_TYPES)} change for {random.choice(['system upgrade', 'patch deployment', 'configuration update', 'security fix'])}",
                'change_type': random.choice(CHANGE_TYPES),
                'risk_level': random.choice(RISK_LEVELS),
                'status': status,
                'requesting_user': str(random.choice(user_ids)),
                'approved_by_user': str(random.choice(user_ids)) if status in ['approved', 'scheduled', 'completed'] else None,
                'scheduled_start_time': scheduled_start.isoformat(),
                'scheduled_end_time': scheduled_end.isoformat(),
                'actual_start_time': actual_start,
                'actual_end_time': actual_end,
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return changes
    
    def generate_rollback_requests(self, changes: Dict, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate rollback requests (for some failed changes)"""
        rollbacks = {}
        incident_ids = list(incidents.keys())
        user_ids = list(users.keys())
        
        # Only create rollbacks for failed or problematic changes
        for change_id, change in changes.items():
            if change['status'] in ['failed', 'rolled_back'] and random.random() > 0.5:
                rollback_id = self.get_next_id('rollbacks')
                
                status = random.choice(ROLLBACK_STATUSES)
                completed_at = None
                if status in ['approved', 'failed']:
                    completed_at = fake.date_time_between(start_date='-1m', end_date='now').isoformat()
                
                rollbacks[rollback_id] = {
                    'rollback_id': str(rollback_id),
                    'change_id': str(change_id),
                    'incident_id': str(random.choice(incident_ids)) if random.random() > 0.6 else None,
                    'requesting_user': str(random.choice(user_ids)),
                    'status': status,
                    'approved_by_user': str(random.choice(user_ids)) if status == 'approved' else None,
                    'completed_at': completed_at,
                    'created_at': fake.date_time_between(start_date='-2m', end_date='now').isoformat()
                }
        
        return rollbacks
    
    def generate_performance_metrics(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate performance metrics (1-4 per incident)"""
        metrics = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            num_metrics = random.randint(1, 4)
            
            for _ in range(num_metrics):
                metric_id = self.get_next_id('metrics')
                
                metric_type = random.choice(METRIC_TYPES)
                
                # Set realistic values based on metric type
                if metric_type == 'response_time':
                    calculated_value = random.randint(5, 120)
                    target = random.choice([15, 30, 60])
                elif metric_type == 'resolution_time':
                    calculated_value = random.randint(60, 2880)
                    target = random.choice([240, 480, 960])
                elif metric_type == 'detection_time':
                    calculated_value = random.randint(1, 60)
                    target = random.choice([5, 10, 30])
                else:  # escalation_time
                    calculated_value = random.randint(30, 480)
                    target = random.choice([60, 120, 240])
                
                recorded_at = fake.date_time_between(start_date='-3m', end_date='now')
                
                metrics[metric_id] = {
                    'metric_id': str(metric_id),
                    'incident_id': str(incident_id),
                    'metric_type': metric_type,
                    'calculated_value_minutes': calculated_value,
                    'target_minutes': target,
                    'recorded_by_user': str(random.choice(user_ids)),
                    'recorded_at': recorded_at.isoformat(),
                    'created_at': recorded_at.isoformat()
                }
        
        return metrics
    
    def generate_incident_reports(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate incident reports (1-2 per incident)"""
        reports = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            num_reports = random.randint(1, 2)
            
            for _ in range(num_reports):
                report_id = self.get_next_id('reports')
                
                generated_at = fake.date_time_between(start_date='-3m', end_date='now')
                
                reports[report_id] = {
                    'report_id': str(report_id),
                    'incident_id': str(incident_id),
                    'report_type': random.choice(REPORT_TYPES),
                    'generated_by_user': str(random.choice(user_ids)),
                    'status': random.choice(REPORT_STATUSES),
                    'generated_at': generated_at.isoformat(),
                    'created_at': generated_at.isoformat()
                }
        
        return reports
    
    def generate_knowledge_base_articles(self, incidents: Dict, users: Dict, count: int = 35) -> Dict[str, Any]:
        """Generate KB articles"""
        articles = {}
        incident_ids = list(incidents.keys())
        user_ids = list(users.keys())
        
        for _ in range(count):
            article_id = self.get_next_id('articles')
            
            created_at, updated_at = generate_timestamps()
            
            status = random.choice(KBA_STATUSES)
            
            articles[article_id] = {
                'article_id': str(article_id),
                'incident_id': str(random.choice(incident_ids)) if random.random() > 0.4 else None,
                'title': f"{random.choice(['How to', 'Guide to', 'Troubleshooting', 'Best practices for', 'Understanding'])} {random.choice(['resolve', 'prevent', 'diagnose', 'handle', 'mitigate'])} {random.choice(INCIDENT_CATEGORIES).lower()} issues",
                'article_type': random.choice(KBA_TYPES),
                'category': random.choice(KBA_CATEGORIES),
                'created_by_user': str(random.choice(user_ids)),
                'reviewer_user': str(random.choice(user_ids)) if status in ['under_review', 'published'] else None,
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return articles
    
    def generate_post_incident_reviews(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate PIR records (for some resolved incidents)"""
        reviews = {}
        user_ids = list(users.keys())
        
        # Only create reviews for resolved/closed incidents
        resolved_incidents = [inc_id for inc_id, inc in incidents.items() 
                             if inc['status'] in ['resolved', 'closed']]
        
        for incident_id in resolved_incidents:
            if random.random() > 0.5:  # 50% chance of review
                review_id = self.get_next_id('reviews')
                
                scheduled_date = fake.date_time_between(start_date='-2m', end_date='+1m')
                status = random.choice(REVIEW_STATUSES)
                
                completed_at = None
                if status == 'completed':
                    completed_at = (scheduled_date + timedelta(days=random.randint(0, 7))).isoformat()
                
                reviews[review_id] = {
                    'review_id': str(review_id),
                    'incident_id': str(incident_id),
                    'facilitator_user': str(random.choice(user_ids)),
                    'scheduled_date': scheduled_date.isoformat(),
                    'overall_rating': random.choice(REVIEW_RATINGS),
                    'status': status,
                    'completed_at': completed_at,
                    'created_at': fake.date_time_between(start_date='-3m', end_date='now').isoformat()
                }
        
        return reviews
    
    def generate_incident_updates(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate incident update records (2-5 per incident)"""
        updates = {}
        user_ids = list(users.keys())
        
        field_types = ['status', 'severity', 'assigned_to', 'impact_level', 'urgency_level']
        
        for incident_id in incidents.keys():
            num_updates = random.randint(2, 5)
            
            for _ in range(num_updates):
                update_id = self.get_next_id('updates')
                
                field = random.choice(field_types)
                
                if field == 'status':
                    old_val = random.choice(['open', 'investigating'])
                    new_val = random.choice(['in_progress', 'resolved'])
                elif field == 'severity':
                    old_val = random.choice(['P3', 'P4'])
                    new_val = random.choice(['P1', 'P2'])
                elif field == 'assigned_to':
                    old_val = str(random.choice(user_ids))
                    new_val = str(random.choice([uid for uid in user_ids if uid != old_val]))
                else:
                    old_val = random.choice(['low', 'medium'])
                    new_val = random.choice(['high', 'critical'])
                
                updates[update_id] = {
                    'update_id': str(update_id),
                    'incident_id': str(incident_id),
                    'updated_by_user': str(random.choice(user_ids)),
                    'update_type': random.choice(['status_change', 'priority_change', 'assignment_change']),
                    'field_changed': field,
                    'old_value': old_val,
                    'new_value': new_val,
                    'created_at': fake.date_time_between(start_date='-3m', end_date='now').isoformat()
                }
        
        return updates
    
    def generate_problem_tickets(self, incidents: Dict, users: Dict) -> Dict[str, Any]:
        """Generate problem tickets (for some incidents)"""
        problems = {}
        user_ids = list(users.keys())
        
        for incident_id in incidents.keys():
            if random.random() > 0.7:  # 30% chance of problem ticket
                problem_id = self.get_next_id('problems')
                
                created_at, updated_at = generate_timestamps()
                
                problems[problem_id] = {
                    'problem_id': str(problem_id),
                    'incident_id': str(incident_id),
                    'title': f"Root cause investigation for recurring {random.choice(INCIDENT_CATEGORIES).lower()} issues",
                    'status': random.choice(INCIDENT_STATUSES),
                    'issued_by_user': str(random.choice(user_ids)),
                    'created_at': created_at,
                    'updated_at': updated_at
                }
        
        return problems
    
    def generate_work_orders(self, incidents: Dict, changes: Dict, problems: Dict, users: Dict, count: int = 40) -> Dict[str, Any]:
        """Generate work order records"""
        work_orders = {}
        incident_ids = list(incidents.keys())
        change_ids = list(changes.keys())
        problem_ids = list(problems.keys())
        user_ids = list(users.keys())
        
        for _ in range(count):
            workorder_id = self.get_next_id('workorders')
            
            created_at, updated_at = generate_timestamps()
            
            # Randomly associate with incident, change, or problem
            assoc_type = random.choice(['incident', 'change', 'problem', 'standalone'])
            
            work_orders[workorder_id] = {
                'workorder_id': str(workorder_id),
                'incident_id': str(random.choice(incident_ids)) if assoc_type == 'incident' and incident_ids else None,
                'change_id': str(random.choice(change_ids)) if assoc_type == 'change' and change_ids else None,
                'problem_id': str(random.choice(problem_ids)) if assoc_type == 'problem' and problem_ids else None,
                'title': f"{random.choice(['Install', 'Configure', 'Replace', 'Update', 'Investigate'])} {random.choice(['hardware', 'software', 'network', 'security', 'database'])} components",
                'work_type': random.choice(['installation', 'configuration', 'maintenance', 'repair', 'investigation']),
                'status': random.choice(WORKORDER_STATUSES),
                'assigned_to_user': str(random.choice(user_ids)) if random.random() > 0.2 else None,
                'created_by_user': str(random.choice(user_ids)),
                'created_at': created_at,
                'updated_at': updated_at
            }
        
        return work_orders
    
    def generate_audit_logs(self, users: Dict, count: int = 100) -> Dict[str, Any]:
        """Generate audit log records"""
        audit_logs = {}
        user_ids = list(users.keys())
        
        actions = ['create', 'update', 'delete', 'view', 'export', 'approve', 'reject', 'escalate']
        entity_types = ['incident', 'user', 'change_request', 'report', 'subscription', 'work_order']
        
        for _ in range(count):
            audit_id = self.get_next_id('audits')
            
            audit_logs[audit_id] = {
                'audit_id': str(audit_id),
                'action': random.choice(actions),
                'entity_type': random.choice(entity_types),
                'entity_id': str(random.randint(1, 50)),
                'audit_by_user': str(random.choice(user_ids)),
                'created_at': fake.date_time_between(start_date='-6m', end_date='now').isoformat()
            }
        
        return audit_logs
    
    def generate_all_data(self):
        """Generate all database records with proper relationships"""
        print("Generating database seed data...")
        
        # Generate independent tables first
        print("- Generating clients...")
        self.data['clients'] = self.generate_clients(15)
        
        print("- Generating vendors...")
        self.data['vendors'] = self.generate_vendors(10)
        
        print("- Generating users...")
        self.data['users'] = self.generate_users(self.data['clients'], self.data['vendors'], 50)
        
        print("- Generating products...")
        self.data['products'] = self.generate_products(self.data['vendors'], 20)
        
        print("- Generating infrastructure components...")
        self.data['infrastructure_components'] = self.generate_infrastructure_components(self.data['products'], 30)
        
        print("- Generating subscriptions...")
        self.data['subscriptions'] = self.generate_subscriptions(self.data['clients'], self.data['products'], 25)
        
        print("- Generating SLAs...")
        self.data['service_level_agreements'] = self.generate_slas(self.data['subscriptions'])
        
        print("- Generating incidents...")
        self.data['incidents'] = self.generate_incidents(self.data['clients'], 
                                                         self.data['infrastructure_components'], 
                                                         self.data['users'], 40)
        
        # Generate dependent tables
        print("- Generating incident escalations...")
        self.data['incident_escalations'] = self.generate_incident_escalations(self.data['incidents'], 
                                                                               self.data['users'])
        
        print("- Generating communications...")
        self.data['communications'] = self.generate_communications(self.data['incidents'], 
                                                                   self.data['users'])
        
        print("- Generating workarounds...")
        self.data['workarounds'] = self.generate_workarounds(self.data['incidents'], 
                                                             self.data['users'])
        
        print("- Generating root cause analyses...")
        self.data['root_cause_analysis'] = self.generate_root_cause_analyses(self.data['incidents'], 
                                                                             self.data['users'])
        
        print("- Generating change requests...")
        self.data['change_requests'] = self.generate_change_requests(self.data['incidents'], 
                                                                     self.data['users'], 30)
        
        print("- Generating rollback requests...")
        self.data['rollback_requests'] = self.generate_rollback_requests(self.data['change_requests'], 
                                                                         self.data['incidents'], 
                                                                         self.data['users'])
        
        print("- Generating performance metrics...")
        self.data['performance_metrics'] = self.generate_performance_metrics(self.data['incidents'], 
                                                                            self.data['users'])
        
        print("- Generating incident reports...")
        self.data['incident_reports'] = self.generate_incident_reports(self.data['incidents'], 
                                                                       self.data['users'])
        
        print("- Generating knowledge base articles...")
        self.data['knowledge_base_articles'] = self.generate_knowledge_base_articles(self.data['incidents'], 
                                                                                     self.data['users'], 35)
        
        print("- Generating post incident reviews...")
        self.data['post_incident_reviews'] = self.generate_post_incident_reviews(self.data['incidents'], 
                                                                                 self.data['users'])
        
        print("- Generating incident updates...")
        self.data['incident_updates'] = self.generate_incident_updates(self.data['incidents'], 
                                                                       self.data['users'])
        
        print("- Generating problem tickets...")
        self.data['problem_tickets'] = self.generate_problem_tickets(self.data['incidents'], 
                                                                     self.data['users'])
        
        print("- Generating work orders...")
        self.data['work_orders'] = self.generate_work_orders(self.data['incidents'], 
                                                             self.data['change_requests'], 
                                                             self.data['problem_tickets'], 
                                                             self.data['users'], 40)
        
        print("- Generating audit logs...")
        self.data['audit_logs'] = self.generate_audit_logs(self.data['users'], 100)
        
        print("Database seed data generation complete!")
        
        return self.data
    
    def save_to_files(self, output_dir: str = 'database_seed'):
        """Save generated data to JSON files"""
        os.makedirs(output_dir, exist_ok=True)
        
        for table_name, table_data in self.data.items():
            file_path = os.path.join(output_dir, f'{table_name}.json')
            with open(file_path, 'w') as f:
                json.dump(table_data, f, indent=2)
            print(f"Saved {table_name}.json ({len(table_data)} records)")

def main():
    """Main execution function"""
    seeder = IncidentManagementSeeder()
    seeder.generate_all_data()
    seeder.save_to_files()
    
    # Print summary statistics
    print("\n=== Generation Summary ===")
    for table_name, table_data in seeder.data.items():
        print(f"{table_name}: {len(table_data)} records")
    
    print("\nAll data has been saved to the 'database_seed' directory.")

if __name__ == "__main__":
    main()