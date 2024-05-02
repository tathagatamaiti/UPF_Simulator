import numpy as np
from event import Event
from events import Events
from ue import UE


class UPF:
    def __init__(self, name, upf_id, start_time, maxnum_pdu, csv_writer):
        self.name = name
        self.upf_id = upf_id  # UPF id
        self.start_time = start_time  # Start time of the UPF
        self.list_pdu = []  # List of PDUs
        self.maxnum_pdu = maxnum_pdu  # Maximum number of PDUs that can be handled by UPF
        self.num_pdus_handled = 0  # Number of PDUs currently being handled
        self.csv_writer = csv_writer

    def can_handle_more_pdus(self):
        return self.num_pdus_handled < self.maxnum_pdu

    def process_pdu_session(self, pdu_session, current_time, scheduler):
        print(f"{Event.event_id_counter}, {np.ceil(scheduler.current_time)}, {self.name} processing {pdu_session}")
        termination_time = np.ceil(UE.pdu_duration)  # Time after which PDU session is to be terminated
        termination_event = Event(current_time + termination_time, Events.PDU_terminate, 3, pdu_session)
        scheduler.schedule_event(termination_event)
        self.num_pdus_handled += 1
        self.csv_writer.writerow([current_time, pdu_session, self.name])  # Write data to CSV

    def terminate_pdu_session(self, pdu_session, scheduler):
        print(f"{Event.event_id_counter}, {np.ceil(scheduler.current_time)}, {pdu_session} terminated")
