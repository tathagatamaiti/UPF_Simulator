from event import Event
from pdu import PDU
import numpy as np


class UE:
    def __init__(self, name):
        self.name = name
        self.next_pdu_session_id = 0

    def generate_pdu_session(self):
        pdu_session = f"{self.name}_pdu{self.next_pdu_session_id}"
        self.next_pdu_session_id += 1
        return pdu_session

    def pdu_session_generation(self, scheduler):
        pdu_session = self.generate_pdu_session()
        pdu_duration = np.random.exponential(scale=5)  # Exponential distribution with scale mu=5
        pdu_request_time = scheduler.current_time + pdu_duration
        PDU(pdu_session, self.name, scheduler.compute_node, scheduler.current_time, pdu_request_time, pdu_duration)
        print(f"Simulation Clock: {scheduler.current_time}, UE {self.name} generated PDU session {pdu_session}")
        print(f"Simulation Clock: {scheduler.current_time}, "
              f"UE {self.name} sends PDU request to Compute Node {scheduler.compute_node.name} "
              f"for PDU session {pdu_session}")
        pdu_request_event = Event(pdu_request_time, 'PDU_request', pdu_session)
        scheduler.schedule_event(pdu_request_event)
        # Schedule next call of pdu_session_generation
        next_arrival_time = scheduler.current_time + np.random.exponential(scale=2)  # Exponential distribution with
        # scale lambda=1
        next_pdu_session_event = Event(next_arrival_time, 'pdu_session_generation', self)
        scheduler.schedule_event(next_pdu_session_event)
