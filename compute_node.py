from upf import UPF

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
        return new_upf

    def process_pdu_requests(self, ue, simulation_clock, event_manager):
        description = f"{simulation_clock:.2f}: Compute Node processing PDU requests"
        event_manager.schedule_event(simulation_clock, description)

        while ue.pdu_queue:
            pdu_session = ue.pdu_queue.pop(0)
            new_upf = self.generate_upf(pdu_session)

            description = f"{simulation_clock:.2f}: {new_upf.upf_id} assigned to process {pdu_session.generate_pdu_id()}"
            event_manager.schedule_event(simulation_clock, description)

            new_upf.process_pdu(pdu_session, simulation_clock, event_manager)
