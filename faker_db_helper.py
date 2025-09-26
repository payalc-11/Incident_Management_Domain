import json
import random
from datetime import datetime, timedelta
from faker import Faker
from typing import Dict, List, Any
import os

fake = Faker()

# Email domains for realistic email generation
EMAIL_DOMAINS = [
    'gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 
    'company.com', 'corp.com', 'enterprise.com', 'tech.com',
    'business.com', 'solutions.com', 'services.com'
]

# US area codes for realistic phone numbers
US_AREA_CODES = [
    '212', '213', '214', '215', '216', '217', '281', '301', '302', '303',
    '305', '310', '312', '313', '314', '315', '404', '405', '407', '408',
    '412', '413', '414', '415', '416', '417', '503', '504', '505', '507',
    '508', '512', '513', '515', '516', '517', '518', '601', '602', '603',
    '605', '607', '608', '609', '612', '614', '615', '616', '617', '618'
]

def generate_phone_number():
    """Generate a realistic US phone number"""
    area_code = random.choice(US_AREA_CODES)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"+1{area_code}{exchange:03d}{number:04d}"

def generate_email(first_name, last_name):
    """Generate a realistic email address"""
    domain = random.choice(EMAIL_DOMAINS)
    formats = [
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name.lower()}{last_name.lower()}@{domain}",
        f"{first_name.lower()}{random.randint(1, 999)}@{domain}",
        f"{last_name.lower()}{random.randint(1, 999)}@{domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{domain}"
    ]
    return random.choice(formats)

def generate_timestamps():
    """Generate created_at and updated_at timestamps with proper ordering"""
    created_at = fake.date_time_between(start_date='-2y', end_date='now')
    updated_at = fake.date_time_between(start_date=created_at, end_date='now')
    return created_at.isoformat(), updated_at.isoformat()

def generate_clients(count=20):
    """Generate client data"""
    clients = {}
    client_types = ['enterprise', 'mid_market', 'small_business', 'startup']
    industries = ['financial_services', 'healthcare', 'technology', 'manufacturing', 
                  'retail', 'education', 'government', 'telecommunications', 'energy', 
                  'transportation', 'media', 'real_estate', 'non_profit']
    statuses = ['active', 'inactive', 'suspended']
    
    for i in range(1, count + 1):
        client_id = str(i)
        company_name = fake.company()
        created_at, updated_at = generate_timestamps()
        
        clients[client_id] = {
            'client_id': client_id,
            'client_name': company_name,
            'registration_number': fake.bothify(text='REG-####-???-####'),
            'client_type': random.choice(client_types),
            'contact_email': f"contact@{company_name.lower().replace(' ', '').replace(',', '').replace('.', '')}.com",
            'contact_phone': generate_phone_number(),
            'industry': random.choice(industries),
            'city': fake.city(),
            'country': fake.country(),
            'timezone': random.choice(['UTC', 'EST', 'PST', 'CST', 'MST']),
            'status': random.choices(statuses, weights=[80, 15, 5])[0],
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return clients

def generate_vendors(count=15):
    """Generate vendor data"""
    vendors = {}
    vendor_types = ['technology_provider', 'infrastructure_provider', 'security_provider',
                   'consulting_services', 'maintenance_services', 'cloud_provider']
    statuses = ['active', 'inactive', 'suspended']
    
    vendor_names = [
        'TechCorp Solutions', 'CloudFirst Systems', 'SecureNet Technologies',
        'DataFlow Consulting', 'InfraTech Services', 'CyberGuard Security',
        'CloudScale Solutions', 'NetworkPro Systems', 'DevOps Masters',
        'ServerTech Inc', 'MonitoringPlus', 'BackupSecure Ltd',
        'DatabasePro Services', 'LoadBalance Systems', 'FirewallExpert Corp'
    ]
    
    for i in range(1, min(count + 1, len(vendor_names) + 1)):
        vendor_id = str(i)
        vendor_name = vendor_names[i-1]
        created_at, updated_at = generate_timestamps()
        
        vendors[vendor_id] = {
            'vendor_id': vendor_id,
            'vendor_name': vendor_name,
            'vendor_type': random.choice(vendor_types),
            'contact_email': f"contact@{vendor_name.lower().replace(' ', '').replace(',', '')}.com",
            'contact_phone': generate_phone_number(),
            'contact_person': fake.name(),
            'status': random.choices(statuses, weights=[85, 10, 5])[0],
            'created_at': created_at
        }
    
    return vendors

def generate_products(vendors, count=25):
    """Generate product data"""
    products = {}
    product_types = ['application', 'database', 'network_service', 'security_service',
                    'monitoring_tool', 'infrastructure_service']
    statuses = ['active', 'deprecated', 'maintenance', 'end_of_life']
    
    product_names = [
        'Enterprise CRM', 'Customer Database', 'Load Balancer Pro', 'Security Scanner',
        'Network Monitor', 'File Storage Service', 'Email Server', 'Web Application',
        'Database Cluster', 'Firewall Manager', 'Backup Service', 'Log Analyzer',
        'Performance Monitor', 'User Directory', 'Payment Gateway', 'Content Delivery',
        'API Gateway', 'Message Queue', 'Cache Service', 'Analytics Platform',
        'Reporting Tool', 'Workflow Engine', 'Document Manager', 'Identity Service',
        'Notification System'
    ]
    
    vendor_ids = list(vendors.keys())
    
    for i in range(1, min(count + 1, len(product_names) + 1)):
        product_id = str(i)
        created_at, updated_at = generate_timestamps()
        
        # 70% chance of having a vendor, 30% internal
        supplier_vendor_id = random.choice(vendor_ids) if random.random() < 0.7 else None
        
        products[product_id] = {
            'product_id': product_id,
            'poduct_name': product_names[i-1],  # Note: keeping the typo as in schema
            'product_type': random.choice(product_types),
            'version': f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            'supplier_vendor_id': supplier_vendor_id,
            'description': '',  # Leaving empty as per rules
            'status': random.choices(statuses, weights=[70, 15, 10, 5])[0],
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return products

def generate_users(clients, vendors, count=30):
    """Generate user data"""
    users = {}
    roles = ['incident_manager', 'technical_support', 'account_manager', 'executive',
            'vendor_contact', 'system_administrator', 'client_contact']
    departments = ['IT Operations', 'Customer Success', 'Engineering', 'Security',
                  'Infrastructure', 'Support', 'Management', 'Business Development']
    statuses = ['active', 'inactive', 'suspended']
    timezones = ['UTC', 'EST', 'PST', 'CST', 'MST', 'GMT']
    
    client_ids = list(clients.keys())
    vendor_ids = list(vendors.keys())
    
    for i in range(1, count + 1):
        user_id = str(i)
        first_name = fake.first_name()
        last_name = fake.last_name()
        role = random.choice(roles)
        created_at, updated_at = generate_timestamps()
        
        # Assign client_id only for client_contact role
        client_id = random.choice(client_ids) if role == 'client_contact' else None
        
        # Assign vendor_id only for vendor_contact role
        vendor_id = random.choice(vendor_ids) if role == 'vendor_contact' else None
        
        users[user_id] = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': generate_email(first_name, last_name),
            'phone_number': generate_phone_number(),
            'role': role,
            'department': random.choice(departments),
            'client_id': client_id,
            'vendor_id': vendor_id,
            'timezone': random.choice(timezones),
            'status': random.choices(statuses, weights=[85, 10, 5])[0],
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return users

def generate_infrastructure_components(products, count=40):
    """Generate infrastructure components"""
    components = {}
    component_types = ['server', 'database', 'network_device', 'load_balancer',
                      'firewall', 'storage', 'application_server']
    environments = ['production', 'staging', 'development', 'testing']
    statuses = ['operational', 'degraded', 'offline', 'maintenance']
    
    product_ids = list(products.keys())
    
    for i in range(1, count + 1):
        component_id = str(i)
        component_type = random.choice(component_types)
        created_at, updated_at = generate_timestamps()
        
        # 80% chance of having a product association
        product_id = random.choice(product_ids) if random.random() < 0.8 else None
        
        components[component_id] = {
            'component_id': component_id,
            'component_name': f"{component_type.replace('_', '-')}-{fake.bothify('??##')}",
            'component_type': component_type,
            'product_id': product_id,
            'environment': random.choice(environments),
            'location': f"Datacenter-{random.choice(['A', 'B', 'C'])}-Rack-{random.randint(1, 20)}",
            'port_number': str(random.choice([80, 443, 8080, 3306, 5432, 6379, 9200])),
            'operational_status': random.choices(statuses, weights=[70, 15, 10, 5])[0],
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return components

def generate_subscriptions(clients, products, count=35):
    """Generate subscription data"""
    subscriptions = {}
    subscription_types = ['full_service', 'limited_service', 'custom', 'trial']
    service_tiers = ['premium', 'standard', 'basic']
    statuses = ['active', 'inactive', 'cancelled', 'expired']
    
    client_ids = list(clients.keys())
    product_ids = list(products.keys())
    
    for i in range(1, count + 1):
        subscription_id = str(i)
        client_id = random.choice(client_ids)
        product_id = random.choice(product_ids)
        
        start_date = fake.date_between(start_date='-1y', end_date='now')
        # 70% chance of ongoing subscription (no end date)
        end_date = None if random.random() < 0.7 else fake.date_between(start_date=start_date, end_date='+1y')
        
        created_at, updated_at = generate_timestamps()
        
        subscriptions[subscription_id] = {
            'subscription_id': subscription_id,
            'client_id': client_id,
            'product_id': product_id,
            'subscription_type': random.choice(subscription_types),
            'service_level_tier': random.choice(service_tiers),
            'recovery_time_objective_hours': random.choice([1, 2, 4, 8, 24]),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'status': random.choices(statuses, weights=[70, 15, 10, 5])[0],
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return subscriptions

def generate_service_level_agreements(subscriptions, count=50):
    """Generate SLA data"""
    slas = {}
    severity_levels = ['P1', 'P2', 'P3', 'P4']
    
    # Response and resolution times by severity
    sla_times = {
        'P1': {'response': [5, 10, 15], 'resolution': [1, 2, 4]},
        'P2': {'response': [15, 30, 60], 'resolution': [4, 8, 12]},
        'P3': {'response': [60, 120, 240], 'resolution': [8, 16, 24]},
        'P4': {'response': [240, 480, 720], 'resolution': [24, 48, 72]}
    }
    
    subscription_ids = list(subscriptions.keys())
    
    for i in range(1, count + 1):
        sla_id = str(i)
        subscription_id = random.choice(subscription_ids)
        severity = random.choice(severity_levels)
        created_at, _ = generate_timestamps()
        
        slas[sla_id] = {
            'sla_id': sla_id,
            'subscription_id': subscription_id,
            'severity_level': severity,
            'response_time_minutes': random.choice(sla_times[severity]['response']),
            'resolution_time_hours': random.choice(sla_times[severity]['resolution']),
            'availability_percentage': round(random.uniform(99.0, 99.99), 2),
            'created_at': created_at
        }
    
    return slas

def generate_incidents(users, clients, components, count=50):
    """Generate incident data"""
    incidents = {}
    categories = ['service_outage', 'performance_degradation', 'security_incident',
                 'data_loss', 'configuration_error', 'hardware_failure']
    severities = ['P1', 'P2', 'P3', 'P4']
    impact_levels = ['critical', 'high', 'medium', 'low']
    statuses = ['open', 'investigating', 'in_progress', 'resolved', 'closed']
    
    # Filter users who can be reporters/assignees
    user_ids = [uid for uid, user in users.items() 
               if user['role'] in ['incident_manager', 'technical_support', 'system_administrator']]
    client_ids = list(clients.keys())
    component_ids = list(components.keys())
    
    incident_titles = [
        'Database Connection Timeout', 'Web Service Unavailable', 'Login System Failure',
        'Network Connectivity Issues', 'Server Performance Degradation', 'SSL Certificate Expired',
        'Load Balancer Malfunction', 'Data Synchronization Error', 'Payment Gateway Down',
        'Email Service Disruption', 'API Rate Limiting Issues', 'File Upload Failures',
        'Search Functionality Broken', 'Memory Leak in Application', 'DNS Resolution Problems',
        'Backup Process Failed', 'Security Alert Triggered', 'User Authentication Error',
        'Database Query Timeout', 'CDN Performance Issues', 'Monitoring System Alert',
        'Service Health Check Failed', 'Third Party Integration Error', 'Cache Invalidation Issue',
        'Mobile App Crash Reports', 'Report Generation Timeout', 'User Session Timeout',
        'Firewall Configuration Error', 'Storage Capacity Warning', 'Application Deployment Issue'
    ]
    
    for i in range(1, count + 1):
        incident_id = str(i)
        reporter_user_id = random.choice(user_ids)
        assigned_to_user_id = random.choice(user_ids) if random.random() < 0.8 else None
        client_id = random.choice(client_ids)
        component_id = random.choice(component_ids) if random.random() < 0.7 else None
        
        detection_timestamp = fake.date_time_between(start_date='-30d', end_date='now')
        status = random.choices(statuses, weights=[10, 15, 25, 30, 20])[0]
        
        # Resolution timestamp only if status is resolved or closed
        resolution_timestamp = None
        if status in ['resolved', 'closed']:
            resolution_timestamp = fake.date_time_between(
                start_date=detection_timestamp,
                end_date='now'
            ).isoformat()
        
        created_at, updated_at = generate_timestamps()
        
        incidents[incident_id] = {
            'incident_id': incident_id,
            'title': random.choice(incident_titles),
            'description': fake.paragraph(nb_sentences=3),
            'category': random.choice(categories),
            'severity': random.choice(severities),
            'impact_level': random.choice(impact_levels),
            'status': status,
            'reporter_user_id': reporter_user_id,
            'assigned_to_user_id': assigned_to_user_id,
            'client_id': client_id,
            'component_id': component_id,
            'detection_timestamp': detection_timestamp.isoformat(),
            'resolution_timestamp': resolution_timestamp,
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return incidents

def generate_problem_tickets(incidents, users, count=30):
    """Generate problem tickets"""
    problem_tickets = {}
    priorities = ['critical', 'high', 'normal', 'low']
    statuses = ['open', 'investigating', 'resolved', 'closed']
    
    incident_ids = list(incidents.keys())
    user_ids = [uid for uid, user in users.items() 
               if user['role'] in ['incident_manager', 'technical_support', 'system_administrator']]
    
    for i in range(1, count + 1):
        problem_id = str(i)
        incident_id = random.choice(incident_ids)
        incident = incidents[incident_id]
        
        created_by_user_id = random.choice(user_ids)
        assigned_to_user_id = random.choice(user_ids) if random.random() < 0.8 else None
        
        created_at, updated_at = generate_timestamps()
        
        problem_tickets[problem_id] = {
            'problem_id': problem_id,
            'incident_id': incident_id,
            'title': f"Root Cause Analysis: {incident['title']}",
            'description': fake.paragraph(nb_sentences=4),
            'technical_details': '',  # Leaving empty as per rules
            'affected_clients_count': random.randint(1, 10),
            'priority': random.choice(priorities),
            'status': random.choice(statuses),
            'created_by_user_id': created_by_user_id,
            'assigned_to_user_id': assigned_to_user_id,
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return problem_tickets

def generate_change_requests(incidents, users, count=40):
    """Generate change requests"""
    change_requests = {}
    change_types = ['emergency', 'normal', 'standard', 'configuration', 'patch', 'upgrade']
    risk_levels = ['high', 'medium', 'low']
    statuses = ['requested', 'approved', 'rejected', 'scheduled', 'in_progress', 'completed', 'failed']
    
    incident_ids = list(incidents.keys())
    user_ids = [uid for uid, user in users.items() 
               if user['role'] in ['incident_manager', 'technical_support', 'system_administrator']]
    
    change_titles = [
        'Update Database Schema', 'Deploy Security Patch', 'Upgrade Server OS',
        'Modify Load Balancer Config', 'Install Monitoring Agent', 'Update SSL Certificates',
        'Configure Firewall Rules', 'Deploy Application Update', 'Restart Database Service',
        'Update Network Configuration', 'Install Security Updates', 'Modify DNS Settings',
        'Update Application Configuration', 'Replace Hardware Component', 'Upgrade Database Version'
    ]
    
    for i in range(1, count + 1):
        change_id = str(i)
        incident_id = random.choice(incident_ids) if random.random() < 0.6 else None
        requesting_user_id = random.choice(user_ids)
        
        status = random.choice(statuses)
        approved_by_user_id = random.choice(user_ids) if status not in ['requested', 'rejected'] else None
        
        # Generate scheduled times if appropriate
        scheduled_start_time = None
        scheduled_end_time = None
        actual_start_time = None
        actual_end_time = None
        
        if status in ['scheduled', 'in_progress', 'completed']:
            scheduled_start = fake.date_time_between(start_date='-7d', end_date='+7d')
            scheduled_start_time = scheduled_start.isoformat()
            scheduled_end_time = (scheduled_start + timedelta(hours=random.randint(1, 8))).isoformat()
            
            if status in ['in_progress', 'completed']:
                actual_start_time = scheduled_start_time
                if status == 'completed':
                    actual_end_time = (scheduled_start + timedelta(hours=random.randint(1, 6))).isoformat()
        
        created_at, updated_at = generate_timestamps()
        
        change_requests[change_id] = {
            'change_id': change_id,
            'incident_id': incident_id,
            'title': random.choice(change_titles),
            'description': fake.paragraph(nb_sentences=3),
            'change_type': random.choice(change_types),
            'risk_level': random.choice(risk_levels),
            'status': status,
            'requesting_user_id': requesting_user_id,
            'approved_by_user_id': approved_by_user_id,
            'scheduled_start_time': scheduled_start_time,
            'scheduled_end_time': scheduled_end_time,
            'actual_start_time': actual_start_time,
            'actual_end_time': actual_end_time,
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return change_requests

def generate_work_orders(change_requests, incidents, users, count=35):
    """Generate work orders"""
    work_orders = {}
    work_types = ['hardware_replacement', 'software_installation', 'configuration_update',
                 'maintenance', 'site_visit']
    priorities = ['urgent', 'high', 'normal', 'low']
    statuses = ['created', 'assigned', 'in_progress', 'completed', 'cancelled']
    
    change_ids = list(change_requests.keys())
    incident_ids = list(incidents.keys())
    user_ids = [uid for uid, user in users.items() 
               if user['role'] in ['technical_support', 'system_administrator']]
    
    work_titles = [
        'Replace Faulty Server', 'Install Security Software', 'Update Network Config',
        'Perform System Maintenance', 'On-site Hardware Check', 'Deploy Application',
        'Configure Load Balancer', 'Update Database Schema', 'Install System Updates',
        'Replace Network Equipment', 'Perform Security Audit', 'Update Firewall Rules'
    ]
    
    for i in range(1, count + 1):
        work_order_id = str(i)
        
        # 60% chance to be related to change request, 30% to incident, 10% standalone
        rand = random.random()
        if rand < 0.6:
            change_id = random.choice(change_ids)
            incident_id = None
        elif rand < 0.9:
            change_id = None
            incident_id = random.choice(incident_ids)
        else:
            change_id = None
            incident_id = None
        
        status = random.choice(statuses)
        assigned_to_user_id = random.choice(user_ids) if status != 'created' else None
        
        estimated_hours = random.randint(1, 16)
        actual_hours = random.randint(1, estimated_hours + 4) if status == 'completed' else None
        
        if status == 'completed':
            scheduled_date = fake.date_between(start_date='-7d', end_date='now')
            completion_date = fake.date_between(start_date=scheduled_date, end_date='now')
        else: 
            scheduled_date = fake.date_between(start_date='-7d', end_date='+14d')
            completion_date = None
     
        created_at, updated_at = generate_timestamps()
        
        work_orders[work_order_id] = {
            'work_order_id': work_order_id,
            'change_id': change_id,
            'incident_id': incident_id,
            'title': random.choice(work_titles),
            'description': fake.paragraph(nb_sentences=2),
            'work_type': random.choice(work_types),
            'priority': random.choice(priorities),
            'status': status,
            'assigned_to_user_id': assigned_to_user_id,
            'estimated_hours': estimated_hours,
            'actual_hours': actual_hours,
            'scheduled_date': scheduled_date.strftime('%Y-%m-%d'),
            'completion_date': completion_date.strftime('%Y-%m-%d') if completion_date else None,
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    return work_orders

def generate_additional_tables(incidents, users, change_requests):
    """Generate data for remaining tables"""
    
    # Incident Escalations
    escalations = {}
    escalation_levels = ['level_1', 'level_2', 'level_3', 'executive']
    escalation_statuses = ['active', 'resolved', 'cancelled']
    
    incident_ids = list(incidents.keys())
    user_ids = list(users.keys())
    
    for i in range(1, 25):
        escalation_id = str(i)
        incident_id = random.choice(incident_ids)
        escalated_from = random.choice(user_ids)
        escalated_to = random.choice([uid for uid in user_ids if uid != escalated_from])
        
        escalated_at = fake.date_time_between(start_date='-30d', end_date='now')
        status = random.choice(escalation_statuses)
        resolved_at = fake.date_time_between(start_date=escalated_at, end_date='now') if status == 'resolved' else None
        
        escalations[escalation_id] = {
            'escalation_id': escalation_id,
            'incident_id': incident_id,
            'escalated_from_user_id': escalated_from,
            'escalated_to_user_id': escalated_to,
            'escalation_level': random.choice(escalation_levels),
            'reason': fake.sentence(nb_words=8),
            'status': status,
            'escalated_at': escalated_at.isoformat(),
            'resolved_at': resolved_at.isoformat() if resolved_at else None
        }
    
    # Communications
    communications = {}
    communication_types = ['status_update', 'escalation_notice', 'resolution_notice', 'workaround_notice']
    recipient_types = ['client_contacts', 'executive_team', 'technical_team', 'all_stakeholders']
    delivery_methods = ['email', 'sms', 'phone', 'chat', 'dashboard_notification']
    delivery_statuses = ['pending', 'sent', 'delivered', 'failed']
    
    for i in range(1, 40):
        communication_id = str(i)
        incident_id = random.choice(incident_ids)
        sender_user_id = random.choice(user_ids)
        
        # Either specific recipient or recipient type
        if random.random() < 0.5:
            recipient_user_id = random.choice([uid for uid in user_ids if uid != sender_user_id])
            recipient_type = None
        else:
            recipient_user_id = None
            recipient_type = random.choice(recipient_types)
        
        sent_at = fake.date_time_between(start_date='-30d', end_date='now')
        
        communications[communication_id] = {
            'communication_id': communication_id,
            'incident_id': incident_id,
            'sender_user_id': sender_user_id,
            'recipient_user_id': recipient_user_id,
            'recipient_type': recipient_type,
            'communication_type': random.choice(communication_types),
            'delivery_method': random.choice(delivery_methods),
            'subject': fake.sentence(nb_words=6),
            'message': fake.paragraph(nb_sentences=3),
            'delivery_status': random.choices(delivery_statuses, weights=[5, 15, 70, 10])[0],
            'sent_at': sent_at.isoformat()
        }
    
    # Performance Metrics
    metrics = {}
    metric_types = ['response_time', 'resolution_time', 'detection_time', 'escalation_time']
    
    for i in range(1, 60):
        metric_id = str(i)
        incident_id = random.choice(incident_ids)
        metric_type = random.choice(metric_types)
        
        # Generate realistic values based on metric type
        if metric_type == 'response_time':
            calculated_value = random.randint(5, 240)
            target_value = random.randint(15, 60)
        elif metric_type == 'resolution_time':
            calculated_value = random.randint(30, 2880)  # 30 min to 48 hours
            target_value = random.randint(60, 1440)  # 1 to 24 hours
        elif metric_type == 'detection_time':
            calculated_value = random.randint(1, 180)
            target_value = random.randint(5, 30)
        else:  # escalation_time
            calculated_value = random.randint(15, 480)
            target_value = random.randint(30, 120)
        
        recorded_at = fake.date_time_between(start_date='-30d', end_date='now')
        
        metrics[metric_id] = {
            'metric_id': metric_id,
            'incident_id': incident_id,
            'metric_type': metric_type,
            'calculated_value_minutes': calculated_value,
            'target_minutes': target_value,
            'recorded_by_user_id': random.choice(user_ids),
            'recorded_at': recorded_at.isoformat()
        }
    
    # Other tables with minimal data
    workarounds = {}
    for i in range(1, 20):
        workaround_id = str(i)
        incident_id = random.choice(incident_ids)
        implemented_at = fake.date_time_between(start_date='-30d', end_date='now')
        created_at = fake.date_time_between(start_date=implemented_at, end_date='now')
        
        workarounds[workaround_id] = {
            'workaround_id': workaround_id,
            'incident_id': incident_id,
            'effectiveness_level': random.choice(['full_mitigation', 'partial_mitigation', 'minimal_impact']),
            'implemented_by_user_id': random.choice(user_ids),
            'status': random.choice(['active', 'superseded', 'obsolete']),
            'implemented_at': implemented_at.isoformat(),
            'created_at': created_at.isoformat()
        }
    
    # Root Cause Analysis
    root_cause_analysis = {}
    analysis_methods = ['five_whys', 'fishbone_diagram', 'fault_tree_analysis', 'timeline_analysis']
    analysis_statuses = ['in_progress', 'completed', 'reviewed']
    
    for i in range(1, 25):
        analysis_id = str(i)
        incident_id = random.choice(incident_ids)
        started_at = fake.date_time_between(start_date='-30d', end_date='now')
        status = random.choice(analysis_statuses)
        completed_at = fake.date_time_between(start_date=started_at, end_date='now') if status in ['completed', 'reviewed'] else None
        
        root_cause_analysis[analysis_id] = {
            'analysis_id': analysis_id,
            'incident_id': incident_id,
            'conducted_by_user_id': random.choice(user_ids),
            'analysis_method': random.choice(analysis_methods),
            'status': status,
            'started_at': started_at.isoformat(),
            'completed_at': completed_at.isoformat() if completed_at else None
        }
    
    # Rollback Requests
    rollback_requests = {}
    rollback_statuses = ['requested', 'approved', 'rejected', 'in_progress', 'completed']
    change_ids = list(change_requests.keys())
    
    for i in range(1, 15):
        rollback_id = str(i)
        change_id = random.choice(change_ids)
        incident_id = random.choice(incident_ids) if random.random() < 0.7 else None
        
        status = random.choice(rollback_statuses)
        approved_by_user_id = random.choice(user_ids) if status not in ['requested', 'rejected'] else None
        created_at = fake.date_time_between(start_date='-30d', end_date='now')
        completed_at = fake.date_time_between(start_date=created_at, end_date='now') if status == 'completed' else None
        
        rollback_requests[rollback_id] = {
            'rollback_id': rollback_id,
            'change_id': change_id,
            'incident_id': incident_id,
            'requesting_user_id': random.choice(user_ids),
            'status': status,
            'approved_by_user_id': approved_by_user_id,
            'created_at': created_at.isoformat(),
            'completed_at': completed_at.isoformat() if completed_at else None
        }
    
    # Incident Reports
    incident_reports = {}
    report_types = ['postmortem', 'executive_summary', 'client_summary', 'technical_analysis']
    report_statuses = ['draft', 'completed', 'reviewed', 'published']
    
    for i in range(1, 30):
        report_id = str(i)
        incident_id = random.choice(incident_ids)
        generated_at = fake.date_time_between(start_date='-30d', end_date='now')
        
        incident_reports[report_id] = {
            'report_id': report_id,
            'incident_id': incident_id,
            'report_type': random.choice(report_types),
            'generated_by_user_id': random.choice(user_ids),
            'status': random.choice(report_statuses),
            'generated_at': generated_at.isoformat()
        }
    
    # Knowledge Base Articles
    kb_articles = {}
    article_types = ['troubleshooting_guide', 'resolution_procedure', 'best_practices', 'lessons_learned']
    kb_categories = ['technical', 'process', 'communication', 'escalation']
    kb_statuses = ['draft', 'under_review', 'published', 'archived']
    
    for i in range(1, 35):
        article_id = str(i)
        incident_id = random.choice(incident_ids) if random.random() < 0.6 else None
        reviewer_user_id = random.choice(user_ids) if random.random() < 0.7 else None
        created_at, updated_at = generate_timestamps()
        
        kb_articles[article_id] = {
            'article_id': article_id,
            'incident_id': incident_id,
            'title': fake.sentence(nb_words=6),
            'article_type': random.choice(article_types),
            'category': random.choice(kb_categories),
            'created_by_user_id': random.choice(user_ids),
            'reviewer_user_id': reviewer_user_id,
            'status': random.choice(kb_statuses),
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    # Post Incident Reviews
    post_reviews = {}
    ratings = ['excellent', 'good', 'satisfactory', 'needs_improvement', 'poor']
    review_statuses = ['scheduled', 'completed', 'cancelled']
    
    for i in range(1, 20):
        review_id = str(i)
        incident_id = random.choice(incident_ids)
        scheduled_date = fake.date_between(start_date='-30d', end_date='+30d')
        
        status = random.choice(review_statuses)
        completed_at = fake.date_time_between(start_date=scheduled_date, end_date='now') if status == 'completed' else None
        created_at = fake.date_time_between(start_date='-45d', end_date='now')
        
        post_reviews[review_id] = {
            'review_id': review_id,
            'incident_id': incident_id,
            'facilitator_user_id': random.choice(user_ids),
            'scheduled_date': scheduled_date.strftime('%Y-%m-%d'),
            'overall_rating': random.choice(ratings),
            'status': status,
            'created_at': created_at.isoformat(),
            'completed_at': completed_at.isoformat() if completed_at else None
        }
    
    # Incident Updates
    incident_updates = {}
    update_types = ['status_change', 'assignment_change', 'severity_change', 'description_update']
    field_names = ['status', 'assigned_to_user_id', 'severity', 'description', 'impact_level']
    
    for i in range(1, 80):
        update_id = str(i)
        incident_id = random.choice(incident_ids)
        field_changed = random.choice(field_names)
        created_at = fake.date_time_between(start_date='-30d', end_date='now')
        
        # Generate realistic old/new values based on field
        if field_changed == 'status':
            old_value = 'open'
            new_value = 'investigating'
        elif field_changed == 'severity':
            old_value = 'P3'
            new_value = 'P2'
        elif field_changed == 'assigned_to_user_id':
            old_value = random.choice(user_ids)
            new_value = random.choice(user_ids)
        else:
            old_value = fake.word()
            new_value = fake.word()
        
        incident_updates[update_id] = {
            'update_id': update_id,
            'incident_id': incident_id,
            'updated_by_user_id': random.choice(user_ids),
            'update_type': random.choice(update_types),
            'field_changed': field_changed,
            'old_value': old_value,
            'new_value': new_value,
            'created_at': created_at.isoformat()
        }
    
    # Audit Logs
    audit_logs = {}
    actions = ['create', 'update', 'delete', 'approve', 'escalate', 'resolve']
    entity_types = ['incident', 'problem_ticket', 'change_request', 'work_order', 'user', 'client', 'vendor', 'product']
    
    for i in range(1, 100):
        audit_id = str(i)
        entity_type = random.choice(entity_types)
        
        # Generate realistic entity_id based on type
        if entity_type == 'incident':
            entity_id = random.choice(incident_ids)
        elif entity_type == 'user':
            entity_id = random.choice(user_ids)
        else:
            entity_id = str(random.randint(1, 50))
        
        created_at = fake.date_time_between(start_date='-60d', end_date='now')
        
        audit_logs[audit_id] = {
            'audit_id': audit_id,
            'user_id': random.choice(user_ids),
            'action': random.choice(actions),
            'entity_type': entity_type,
            'entity_id': entity_id,
            'created_at': created_at.isoformat()
        }
    
    return {
        'incident_escalations': escalations,
        'communications': communications,
        'workarounds': workarounds,
        'root_cause_analysis': root_cause_analysis,
        'performance_metrics': metrics,
        'rollback_requests': rollback_requests,
        'incident_reports': incident_reports,
        'knowledge_base_articles': kb_articles,
        'post_incident_reviews': post_reviews,
        'incident_updates': incident_updates,
        'audit_logs': audit_logs
    }

def main():
    """Main function to generate all data and save to JSON files"""
    print("Generating incident management system data...")
    
    # Create output directory
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate data in dependency order
    print("Generating clients...")
    clients = generate_clients(20)
    
    print("Generating vendors...")
    vendors = generate_vendors(15)
    
    print("Generating products...")
    products = generate_products(vendors, 25)
    
    print("Generating users...")
    users = generate_users(clients, vendors, 30)
    
    print("Generating infrastructure components...")
    infrastructure_components = generate_infrastructure_components(products, 40)
    
    print("Generating subscriptions...")
    subscriptions = generate_subscriptions(clients, products, 35)
    
    print("Generating service level agreements...")
    service_level_agreements = generate_service_level_agreements(subscriptions, 50)
    
    print("Generating incidents...")
    incidents = generate_incidents(users, clients, infrastructure_components, 50)
    
    print("Generating problem tickets...")
    problem_tickets = generate_problem_tickets(incidents, users, 30)
    
    print("Generating change requests...")
    change_requests = generate_change_requests(incidents, users, 40)
    
    print("Generating work orders...")
    work_orders = generate_work_orders(change_requests, incidents, users, 35)
    
    print("Generating additional tables...")
    additional_tables = generate_additional_tables(incidents, users, change_requests)
    
    # Combine all data
    all_data = {
        'clients': clients,
        'vendors': vendors,
        'products': products,
        'users': users,
        'infrastructure_components': infrastructure_components,
        'subscriptions': subscriptions,
        'service_level_agreements': service_level_agreements,
        'incidents': incidents,
        'problem_tickets': problem_tickets,
        'change_requests': change_requests,
        'work_orders': work_orders,
        **additional_tables
    }
    
    # Save each table to separate JSON file
    for table_name, table_data in all_data.items():
        filename = os.path.join(output_dir, f"{table_name}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(table_data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(table_data)} records to {filename}")
    
    print(f"\nData generation complete! All files saved to '{output_dir}' directory.")
    
    # Print summary statistics
    print("\nGenerated data summary:")
    for table_name, table_data in all_data.items():
        print(f"  {table_name}: {len(table_data)} records")

if __name__ == "__main__":
    main()