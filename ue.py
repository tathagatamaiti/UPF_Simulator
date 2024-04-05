from event import Event
from events import Events
from pdu import PDU
import numpy as np


class UE:
    pdu_duration = np.random.exponential(scale=5)  # Duration of the PDU session

    def __init__(self, name):
        self.name = name
        self.pdu_session_id = 0  # PDU id

    def generate_pdu_session(self):
        pdu_session = f"{self.name}_pdu{self.pdu_session_id}"  # PDU session generated by the UE
        self.pdu_session_id += 1
        return pdu_session

    def pdu_session_generation(self, scheduler):
        pdu_id = self.pdu_session_id
        pdu_class = None  # Class of PDU being generated
        pdu_session = self.generate_pdu_session()
        pdu_duration = np.ceil(np.random.exponential(scale=5))  # Exponential distribution with scale mu=5
        pdu_start_time = np.ceil(scheduler.current_time)  # Start time of the PDU session
        PDU(pdu_id, pdu_class, self.name, scheduler.compute_node, pdu_start_time, pdu_duration)
        print(f"{np.ceil(scheduler.current_time)}, {self.name} generated {pdu_session}")
        print(f"{np.ceil(scheduler.current_time)}, "
              f"{self.name} sends PDU request to {scheduler.compute_node.name} "
              f"for {pdu_session}")
        pdu_request_event = Event(pdu_start_time, Events.PDU_request, pdu_session)
        scheduler.schedule_event(pdu_request_event)
        # Schedule next call of pdu_session_generation
        next_arrival_time = np.ceil(scheduler.current_time + np.random.exponential(scale=2))  # Exponential
        # distribution with
        # scale lambda=2
        next_pdu_session_event = Event(next_arrival_time, Events.PDU_session_generation, self)
        scheduler.schedule_event(next_pdu_session_event)
