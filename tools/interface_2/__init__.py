from .add_component import AddComponent
from .add_product import AddProduct
from .conduct_rca import ConductRca
from .add_client_subscription import AddClientSubscription
from .create_vendor import CreateVendor
from .discover_component import DiscoverComponent
from .discover_incident import DiscoverIncident
from .discover_product import DiscoverProduct
from .discover_vendor import DiscoverVendor
from .create_audit import CreateAudit
from .log_incident_update import LogIncidentUpdate
from .record_communication import RecordCommunication
from .record_workaround import RecordWorkaround
from .file_incident import FileIncident
from .submit_escalation import SubmitEscalation
from .update_incident import UpdateIncident

ALL_TOOLS_INTERFACE_2 = [
    AddComponent,
    AddProduct,
    ConductRca,
    AddClientSubscription,
    CreateVendor,
    DiscoverComponent,
    DiscoverIncident,
    DiscoverProduct,
    DiscoverVendor,
    CreateAudit,
    LogIncidentUpdate,
    RecordCommunication,
    RecordWorkaround,
    FileIncident,
    SubmitEscalation,
    UpdateIncident
]
