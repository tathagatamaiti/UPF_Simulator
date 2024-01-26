class UPF:
    def __init__(self, upf_id):
        self.upf_id = upf_id
        self.start_time = None

    def process_pdu(self, pdu_session, simulation_clock, event_manager):
        pdu_session.start_time = simulation_clock
        pdu_session.associate_upf(self)

        description = f"{simulation_clock:.2f}: {self.upf_id} processing {pdu_session.generate_pdu_id()}"
        event_manager.schedule_event(simulation_clock, description)

        description = f"{simulation_clock:.2f}: {self.upf_id} completed processing {pdu_session.generate_pdu_id()}"
        event_manager.schedule_event(simulation_clock, description)

        pdu_session.terminate_pdu()
        self.terminate_upf(simulation_clock, event_manager)

    def terminate_upf(self, simulation_clock, event_manager):
        description = f"{simulation_clock:.2f}: {self.upf_id} terminated"
        event_manager.schedule_event(simulation_clock, description)
