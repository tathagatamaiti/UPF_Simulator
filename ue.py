import numpy as np
from pdu import PDU


class UE:
    def __init__(self, compute_node, event_manager, ue_id):
        self.mean_pdu_arrival_time = 10
        self.ue_id = ue_id
        self.compute_node = compute_node
        self.event_manager = event_manager

    def generate_pdu_sessions(self, simulation_clock, event_manager):
        time_to_next_pdu = np.random.exponential(self.mean_pdu_arrival_time)
        next_pdu_time = simulation_clock + time_to_next_pdu

        pdu_duration = 5
        pdu_data = f"PDU data for UE{self.ue_id}"
        pdu_session = PDU(self.ue_id, pdu_data, pdu_duration)
        pdu_session.start_time = next_pdu_time

        description = f"UE{self.ue_id} generates PDU session: {pdu_session.generate_pdu_id()}"
        event = self.event_manager.create_event(next_pdu_time, "UE_GENERATE_PDU_SESSION", description, self)
        self.event_manager.schedule_event(event)

        description = f"UE{self.ue_id} sends PDU request {pdu_session.generate_pdu_id()} to Compute Node"
        event = self.event_manager.create_event(next_pdu_time, "UE_SEND_PDU_REQUEST", description, self)
        self.event_manager.schedule_event(event)

        return next_pdu_time < self.event_manager.get_simulation_time()
