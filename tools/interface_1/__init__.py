from .create_client_subscription import CreateClientSubscription
from .create_client import CreateClient
from .create_sla_record import CreateSlaRecord
from .discover_client import DiscoverClient
from .discover_subscription import DiscoverSubscription
from .discover_user import DiscoverUser
from .generate_incident_report import GenerateIncidentReport
from .log_audit import LogAudit
from .log_metric import LogMetric
from .manage_sla_record import ManageSlaRecord
from .record_kb_article import RecordKbArticle
from .register_user import RegisterUser
from .report_incident import ReportIncident
from .update_client import UpdateClient
from .update_user import UpdateUser

ALL_TOOLS_INTERFACE_1 = [
    CreateClientSubscription,
    CreateClient,
    CreateSlaRecord,
    DiscoverClient,
    DiscoverSubscription,
    DiscoverUser,
    GenerateIncidentReport,
    LogAudit,
    LogMetric,
    ManageSlaRecord,
    RecordKbArticle,
    RegisterUser,
    ReportIncident,
    UpdateClient,
    UpdateUser
]
