from event import Event
from ue import UE


class UPF:

    def __init__(self, name, upf_id, start_time, maxnum_pdu):
        self.name = name
        self.upf_id = upf_id  # UPF id
        self.start_time = start_time  # Start time of the UPF
        self.list_pdu = []  # List of PDUs
        self.maxnum_pdu = maxnum_pdu  # Maximum number of PDUs in the experiment

    def process_pdu_session(self, pdu_session, current_time, scheduler):
        print(f"{current_time}, {self.name} processing {pdu_session}")
        termination_time = UE.pdu_duration  # Time after which PDU session is to be terminated
        termination_event = Event(current_time + termination_time, 'PDU_terminate', pdu_session)
        scheduler.schedule_event(termination_event)

    def terminate_pdu_session(self, pdu_session, scheduler):
        print(f"{scheduler.current_time}, {pdu_session} terminated")

    def terminate(self, scheduler):
        print(f"{scheduler.current_time}, {self.name} terminated")
