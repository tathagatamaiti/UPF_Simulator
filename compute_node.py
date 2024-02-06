from upf import UPF
from event import Event
from events import Events


class ComputeNode:
    def __init__(self, event_manager):
        self.upfs = []
        self.next_upf_id = 0
        self.event_manager = event_manager

    def add_upf(self, upf):
        self.upfs.append(upf)

    def generate_upf(self, pdu_session, max_pdus_per_upf):
        new_upf_id = self.next_upf_id
        self.next_upf_id += 1
        new_upf = UPF(new_upf_id, max_pdus_per_upf)
        self.add_upf(new_upf)
        return new_upf

    def process_pdu_requests(self, ue, simulation_clock, event_manager):
        while ue.pdu_queue:
            pdu_session = ue.pdu_queue.pop(0)
            new_upf = self.generate_upf(pdu_session, max_pdus_per_upf=2)

            description = f"UPF{new_upf.upf_id} assigned to process {pdu_session.generate_pdu_id()}"
            event = Event(simulation_clock, Events.UPF_PROCESS_PDU, description)
            event_manager.schedule_event(event)

            new_upf.process_next_pdu(pdu_session, simulation_clock + 1, event_manager)
