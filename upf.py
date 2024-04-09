import numpy as np

from event import Event
from events import Events
from ue import UE


class UPF:
    def __init__(self, name, upf_id, start_time, maxnum_pdu):
        self.name = name
        self.upf_id = upf_id  # UPF id
        self.start_time = start_time  # Start time of the UPF
        self.list_pdu = []  # List of PDUs
        self.maxnum_pdu = maxnum_pdu  # Maximum number of PDUs that can be handled by UPF
        self.num_pdus_handled = 0  # Number of PDUs currently being handled

    def can_handle_more_pdus(self):
        return self.num_pdus_handled < self.maxnum_pdu

    def process_pdu_session(self, pdu_session, current_time, scheduler):
        if self.can_handle_more_pdus():
            print(f"{np.ceil(scheduler.current_time)}, {self.name} processing {pdu_session}")
            termination_time = np.ceil(UE.pdu_duration)  # Time after which PDU session is to be terminated
            termination_event = Event(current_time + termination_time, Events.PDU_terminate, 3, pdu_session)
            scheduler.schedule_event(termination_event)
            self.num_pdus_handled += 1
        else:
            new_upf_id = self.upf_id + 1
            new_upf_name = f"{scheduler.compute_node.name}_UPF{new_upf_id}"
            new_upf = UPF(new_upf_name, new_upf_id, current_time, self.maxnum_pdu)
            scheduler.compute_node.list_upf.append(new_upf)
            new_upf.process_pdu_session(pdu_session, current_time, scheduler)

    def terminate_pdu_session(self, pdu_session, scheduler):
        print(f"{np.ceil(scheduler.current_time)}, {pdu_session} terminated")
        self.num_pdus_handled -= 1

#        if self.num_pdus_handled == 0:
#            termination_event = Event(scheduler.current_time + 1, Events.UPF_terminate, 4, self)
#            scheduler.schedule_event(termination_event)
