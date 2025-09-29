from .record_rca import RecordRca
from .create_ticket import CreateTicket
from .create_workorder import CreateWorkorder
from .get_incident import GetIncident
from .get_user import GetUser
from .write_audit import WriteAudit
from .add_incident_update import AddIncidentUpdate
from .add_communication import AddCommunication
from .add_workaround import AddWorkaround
from .create_escalation import CreateEscalation
from .transfer_to_human import TransferToHuman
from .amend_incident import AmendIncident
from .update_ticket import UpdateTicket
from .amend_user import AmendUser
from .update_workorder import UpdateWorkorder

ALL_TOOLS_INTERFACE_3 = [
    RecordRca,
    CreateTicket,
    CreateWorkorder,
    WriteAudit,
    AddIncidentUpdate,
    AddCommunication,
    AddWorkaround,
    CreateEscalation,
    TransferToHuman,
    AmendIncident,
    UpdateTicket,
    AmendUser,
    UpdateWorkorder,
    GetIncident,
    GetUser
]
