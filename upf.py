from event import Event
from events import Events


class UPF:
    def __init__(self, upf_id):
        self.upf_id = upf_id
        self.start_time = None

    def process_pdu(self, pdu_session, simulation_clock, event_manager):
        pdu_session.start_time = simulation_clock
        pdu_session.associate_upf(self)

        description = f"{self.upf_id} processing {pdu_session.generate_pdu_id()}"
        event = Event(simulation_clock, Events.UPF_PROCESS_PDU, description)
        event_manager.schedule_event(event)

        description = f"{self.upf_id} completed processing {pdu_session.generate_pdu_id()}"
        event = Event(simulation_clock, Events.PDU_SESSION_TERMINATE, description)
        event_manager.schedule_event(event)

        pdu_session.terminate_pdu(simulation_clock, event_manager)
        self.terminate_upf(simulation_clock, event_manager)

    def terminate_upf(self, simulation_clock, event_manager):
        description = f"{self.upf_id} terminated"
        event = Event(simulation_clock, Events.UPF_TERMINATE, description)
        event_manager.schedule_event(event)