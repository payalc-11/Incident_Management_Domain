from .create_component import CreateComponent
from .create_product import CreateProduct
from .create_user import CreateUser
from .escalate_to_human import EscalateToHuman
from .register_client import RegisterClient
from .register_vendor import RegisterVendor
from .register_workorder import RegisterWorkorder
from .fetch_client import FetchClient
from .fetch_component import FetchComponent
from .fetch_product import FetchProduct
from .fetch_subscription import FetchSubscription
from .fetch_user import FetchUser
from .fetch_vendor import FetchVendor
from .register_incident_report import RegisterIncidentReport
from .record_audit import RecordAudit
from .make_sla_record import MakeSlaRecord
from .register_communication import RegisterCommunication
from .register_kb_article import RegisterKbArticle
from .register_change_request import RegisterChangeRequest
from .register_escalation import RegisterEscalation
from .register_post_incident_review import RegisterPostIncidentReview
from .submit_rollback_request import SubmitRollbackRequest


ALL_TOOLS_INTERFACE_5 = [
    CreateComponent,
    CreateProduct,
    CreateUser,
    EscalateToHuman,
    RegisterClient,
    RegisterVendor,
    RegisterWorkorder,
    FetchClient,
    FetchComponent,
    FetchProduct,
    FetchSubscription,
    FetchUser,
    FetchVendor,
    RegisterIncidentReport,
    RecordAudit,
    MakeSlaRecord,
    RegisterCommunication,
    RegisterKbArticle,
    RegisterChangeRequest,
    RegisterEscalation,
    RegisterPostIncidentReview,
    SubmitRollbackRequest
]
