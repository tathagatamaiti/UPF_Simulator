from event import Event, EventType
from pdu import PDU
import numpy as np


class UE:
    def __init__(self, compute_node, event_manager):
        self.compute_node = compute_node
        self.event_manager = event_manager

    def initialize_event(self):
        return Event(0, EventType.UE_INITIALIZATION, "UE Initialization", source="UE", destination="Compute Node")

    def generate_pdu_sessions(self, simulation_clock):
        time_to_next_pdu = np.random.exponential(10)
        next_pdu_time = simulation_clock + time_to_next_pdu
        pdu_duration = 5

        pdu_data = f"PDU data for UE"
        pdu_session = PDU(pdu_data, pdu_duration)

        description = f"UE generates PDU session: {pdu_session.generate_pdu_id()}"
        event = Event(next_pdu_time, EventType.PDU_GENERATION, description, source="UE", destination="Compute Node")
        self.event_manager.schedule_event(event, pdu_session)

    def handle_event(self, event):
        if event.event_type == EventType.UE_INITIALIZATION:
            self.generate_pdu_sessions(event.event_time)
        elif event.event_type == EventType.PDU_GENERATION:
            pdu_session = event.data
            self.compute_node.process_pdu_request(pdu_session, event.event_time, self.event_manager)
