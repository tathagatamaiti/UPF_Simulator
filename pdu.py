class PDU:
    def __init__(self, ue_id, pdu_data, counter):
        self.ue_id = ue_id
        self.pdu_data = pdu_data
        self.counter = counter
        self.start_time = None
        self.upf = None

    def generate_pdu_id(self):
        return f"PDU_{self.ue_id}_{self.counter}"

    def associate_upf(self, upf):
        self.upf = upf

    def terminate_pdu(self, event_manager, simulation_clock):
        event_manager.schedule_event(simulation_clock, f"{self.generate_pdu_id()} terminated after processing")

    def __str__(self):
        return f"{self.start_time:.2f}: {self.generate_pdu_id()} - {self.pdu_data}"
