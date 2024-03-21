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
        if len(self.list_pdu) + 1 > self.maxnum_pdu:
            # Reject PDU request
            print(f"Simulation Clock: {current_time}, UPF {self.name} rejected PDU session {pdu_session}")
            termination_event = Event(current_time, 'PDU_terminate', pdu_session, "REJECT")
            scheduler.schedule_event(termination_event)
        else:
            # Accept PDU request
            print(f"Simulation Clock: {current_time}, UPF {self.name} accepted PDU session {pdu_session}")
            print(f"Simulation Clock: {current_time}, UPF {self.name} processing PDU session {pdu_session}")
            termination_time = UE.pdu_duration  # Time after which PDU session is to be terminated
            self.list_pdu.append(pdu_session)
            termination_event = Event(current_time + termination_time, 'PDU_terminate', pdu_session, "ACCEPT")
            scheduler.schedule_event(termination_event)

    def terminate_pdu_session(self, pdu_session, scheduler, termination_type):
        if termination_type == "ACCEPT":
            self.list_pdu.remove(pdu_session)
            print(f"Simulation Clock: {scheduler.current_time}, PDU session {pdu_session} terminated")
        else:
            print(f"Simulation Clock: {scheduler.current_time}, PDU session {pdu_session} rejected")

    def terminate(self, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, UPF {self.name} terminated")
