from upf import UPF
from event import Event
from events import Events


class ComputeNode:
    def __init__(self, event_manager):
        self.upfs = []
        self.event_manager = event_manager

    def add_upf(self, upf):
        self.upfs.append(upf)

    def generate_upf(self, pdu_session):
        new_upf_id = f"UPF_{pdu_session.generate_pdu_id()}"
        new_upf = UPF(new_upf_id)
        self.add_upf(new_upf)

        description = f"Compute Node allocated UPF for PDU session: {new_upf.upf_id}"
        event = Event(self.event_manager.get_simulation_clock(), Events.COMPUTE_NODE_ALLOCATE_UPF, description)
        self.event_manager.schedule_event(event)

        return new_upf

    def process_pdu_requests(self, ue, simulation_clock, event_manager):
        while ue.pdu_queue:
            pdu_session = ue.pdu_queue.pop(0)
            new_upf = self.generate_upf(pdu_session)

            description = (f"{new_upf.upf_id} assigned to process "
                           f"{pdu_session.generate_pdu_id()}")
            event = Event(simulation_clock, Events.UPF_PROCESS_PDU, description)
            event_manager.schedule_event(event)

            new_upf.process_pdu(pdu_session, simulation_clock, event_manager)