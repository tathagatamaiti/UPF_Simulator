import numpy as np
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
        inter_arrival_time = np.random.poisson(lam=3)
        next_pdu_time = simulation_clock + inter_arrival_time

        pdu_duration = 5

        pdu_data = f"PDU data for UE"
        pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter, pdu_duration)
        pdu_session.start_time = next_pdu_time
        description = f"UE{self.ue_id} generates PDU session: {pdu_session.generate_pdu_id()}"
        event = Event(next_pdu_time, Events.UE_GENERATE_PDU_SESSION, description)
        event_manager.schedule_event(event)

        self.pdu_counter += 1
        self.pdu_queue.append(pdu_session)

        description = f"UE{self.ue_id} sends PDU request {pdu_session.generate_pdu_id()} to Compute Node"
        event = Event(next_pdu_time, Events.UE_SEND_PDU_REQUEST, description)
        event_manager.schedule_event(event)

        self.compute_node.process_pdu_requests(self, next_pdu_time, event_manager)

        terminate_time = next_pdu_time + pdu_duration
        description = f"{pdu_session.generate_pdu_id()} termination"
        terminate_event = Event(terminate_time, Events.PDU_SESSION_TERMINATE, description)
        event_manager.schedule_event(terminate_event)

        return self.pdu_counter < self.pdu_limit
