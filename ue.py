from pdu import PDU
from event import Event
from events import Events


class UE:
    def __init__(self, compute_node, pdu_limit, event_manager):
        self.ue_id = 1
        self.compute_node = compute_node
        self.pdu_counter = 0
        self.pdu_limit = pdu_limit
        self.pdu_queue = []
        self.event_manager = event_manager

    def generate_pdu_sessions(self, simulation_clock, event_manager):
        pdu_data = f"PDU data for UE"
        pdu_duration = 5
        pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter, pdu_duration)
        pdu_session.start_time = simulation_clock
        description = f"UE{self.ue_id} generates PDU session: {pdu_session}"
        event = Event(simulation_clock, Events.UE_GENERATE_PDU_SESSION, description)
        event_manager.schedule_event(event)

        self.pdu_counter += 1
        self.pdu_queue.append(pdu_session)

        description = f"UE{self.ue_id} sends PDU request {pdu_session} to Compute Node"
        event = Event(simulation_clock, Events.UE_SEND_PDU_REQUEST, description)
        event_manager.schedule_event(event)
        self.compute_node.process_pdu_requests(self, simulation_clock, event_manager)

        return self.pdu_counter < self.pdu_limit
