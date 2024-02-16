class EventType:
    UE_INITIALIZATION = "UE Initialization"
    PDU_GENERATION = "PDU Generation"
    UPF_ALLOCATION = "UPF Allocation"
    UPF_PROCESSING = "UPF Processing"
    PDU_TERMINATION = "PDU Termination"


class Event:
    def __init__(self, event_time, event_type, description, source=None, destination=None):
        self.event_time = event_time
        self.event_type = event_type
        self.description = description
        self.source = source
        self.destination = destination
        self.data = None

    def handle_event(self, manager):
        pass
