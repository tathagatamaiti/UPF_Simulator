from event import Event
from events import Events


class UPF:
    def __init__(self, upf_id, max_pdus_per_upf):
        self.upf_id = upf_id
        self.start_time = None
        self.max_pdus_per_upf = max_pdus_per_upf
        self.processed_pdus = 0
        self.assigned_pdus = []

    def process_pdu(self, pdu_session, simulation_clock, event_manager):
        pdu_session.start_time = simulation_clock
        pdu_session.associate_upf(self)

        description = f"UPF{self.upf_id} processing {pdu_session.generate_pdu_id()}"
        event = Event(simulation_clock, Events.UPF_PROCESS_PDU, description)
        event_manager.schedule_event(event)

        self.processed_pdus += 1
        self.assigned_pdus.append(pdu_session)

        if self.processed_pdus >= self.max_pdus_per_upf:
            self.terminate_upf(simulation_clock, event_manager)
        else:
            description = f"UPF{self.upf_id} completed processing {pdu_session.generate_pdu_id()}"
            completion_event = Event(simulation_clock, Events.PDU_SESSION_TERMINATE, description)
            event_manager.schedule_event(completion_event)

    def terminate_upf(self, simulation_clock, event_manager):
        for pdu_session in self.assigned_pdus:
            description = f"{pdu_session.generate_pdu_id()} termination"
            terminate_event = Event(simulation_clock, Events.PDU_SESSION_TERMINATE, description)
            event_manager.schedule_event(terminate_event)

        description = f"UPF{self.upf_id} terminated"
        event = Event(simulation_clock, Events.UPF_TERMINATE, description)
        event_manager.schedule_event(event)

    def process_next_pdu(self, pdu_session, simulation_clock, event_manager):
        self.process_pdu(pdu_session, simulation_clock, event_manager)
