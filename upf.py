from event import Event
import random


class UPF:
    def __init__(self, name):
        self.name = name

    def process_pdu_session(self, pdu_session, current_time, scheduler):
        print(f"Simulation Clock: {current_time}, UPF {self.name} processing PDU session {pdu_session}")
        termination_time = random.randint(5, 10)
        termination_event = Event(current_time + termination_time, 'PDU_terminate', pdu_session)
        scheduler.schedule_event(termination_event)

    def terminate_pdu_session(self, pdu_session, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, PDU session {pdu_session} terminated")

    def terminate(self, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, UPF {self.name} terminated")
