from event import Event, EventType
from upf import UPF


class ComputeNode:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.upfs = []

    def process_pdu_request(self, pdu_session, simulation_clock):
        if len(self.upfs) == 0 or self.upfs[-1].processed_pdus >= self.upfs[-1].max_pdus_per_upf:
            new_upf = UPF(len(self.upfs), 2)
            self.upfs.append(new_upf)

            description = f"Compute Node allocated UPF{new_upf.upf_id} for PDU session"
            event = Event(simulation_clock, EventType.UPF_ALLOCATION, description, source="Compute Node",
                          destination=f"UPF{new_upf.upf_id}")
            self.event_manager.schedule_event(event, pdu_session)
        else:
            description = f"Compute Node allocated UPF{self.upfs[-1].upf_id} for PDU session"
            event = Event(simulation_clock, EventType.UPF_ALLOCATION, description, source="Compute Node",
                          destination=f"UPF{self.upfs[-1].upf_id}")
            self.event_manager.schedule_event(event, pdu_session)

    def handle_event(self, event):
        if event.event_type == EventType.UPF_ALLOCATION:
            pdu_session = event.data
            upf_id = int(event.destination.split("UPF")[1])
            upf = self.upfs[upf_id]
            upf.process_pdu(pdu_session, event.event_time)
