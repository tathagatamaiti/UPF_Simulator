class UPF:
    def __init__(self, upf_id, event_manager):
        self.upf_id = upf_id
        self.start_time = None
        self.event_manager = event_manager

    def process_pdu(self, pdu_session, simulation_clock):
        pdu_session.start_time = simulation_clock
        pdu_session.associate_upf(self)

        self.event_manager.schedule_event(simulation_clock, f"{self.upf_id} processing {pdu_session}")

        self.event_manager.schedule_event(simulation_clock, f"{self.upf_id} completed processing {pdu_session}")
        pdu_session.terminate_pdu(self.event_manager, simulation_clock)
