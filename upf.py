from event import Event, EventType


class UPF:
    def __init__(self, upf_id, max_pdus_per_upf, event_manager):
        self.upf_id = upf_id
        self.max_pdus_per_upf = max_pdus_per_upf
        self.processed_pdus = 0
        self.event_manager = event_manager  # Added event_manager argument

    def process_pdu(self, pdu_session, simulation_clock):
        description = f"UPF{self.upf_id} processing {pdu_session.generate_pdu_id()}"
        event = Event(simulation_clock, EventType.UPF_PROCESSING, description, source=f"UPF{self.upf_id}",
                      destination="UE")
        pdu_session.start_time = simulation_clock
        self.processed_pdus += 1
        if self.processed_pdus >= self.max_pdus_per_upf:
            pdu_termination_event = Event(simulation_clock + pdu_session.duration, EventType.PDU_TERMINATION,
                                          f"PDU termination: {pdu_session.generate_pdu_id()}", source="UPF",
                                          destination="UE")
            self.processed_pdus = 0
            self.event_manager.schedule_event(pdu_termination_event)
        return event
