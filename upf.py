from event import Event
from ue import UE


class UPF:

    # DEFINING EXPERIMENT PARAMETERS
    maxnum_pdu = "MAXIMUM NUMBER OF PDUs IN THE EXPERIMENT"
    termination_time = "TIME AFTER WHICH PDU SESSION IS TO BE TERMINATED"

    def __init__(self, name, upf_id, start_time, maxnum_pdu):
        self.name = name
        self.upf_id = upf_id
        self.start_time = start_time
        self.list_pdu = []
        self.maxnum_pdu = maxnum_pdu

    def process_pdu_session(self, pdu_session, current_time, scheduler):
        print(f"Simulation Clock: {current_time}, UPF {self.name} processing PDU session {pdu_session}")
        termination_time = UE.pdu_duration
        termination_event = Event(current_time + termination_time, 'PDU_terminate', pdu_session)
        scheduler.schedule_event(termination_event)

    def terminate_pdu_session(self, pdu_session, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, PDU session {pdu_session} terminated")

    def terminate(self, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, UPF {self.name} terminated")
