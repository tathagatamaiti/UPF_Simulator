class PDU:
    def __init__(self, ue_id, pdu_data, duration):
        self.ue_id = ue_id
        self.pdu_data = pdu_data
        self.duration = duration
        self.start_time = None
        self.upf = None

    def generate_pdu_id(self):
        return f"PDU_{self.ue_id}_{self.start_time}"

    def associate_upf(self, upf):
        self.upf = upf

    def terminate(self, event_manager, simulation_clock):
        description = f"{self.generate_pdu_id()} termination"
        terminate_event = event_manager.create_event(simulation_clock, "PDU_SESSION_TERMINATE", description, self)
        event_manager.schedule_event(terminate_event)

    def __str__(self):
        if self.start_time is not None:
            return (
                f"{self.start_time:.2f}: {self.generate_pdu_id()} - {self.pdu_data} (Duration: {self.duration} seconds)"
            )
        else:
            return f"{self.generate_pdu_id()} - {self.pdu_data} (Duration: {self.duration} seconds)"
