import heapq
from event import Event
from events import Events
import plots
from upf import UPF


class Scheduler:

    def __init__(self, total_simulation_time):
        self.compute_node = None  # Compute Node in experiment
        self.ue_list = []  # List of UEs
        self.events = []  # List of events
        self.total_simulation_time = total_simulation_time  # Total simulation time for the experiment
        self.current_time = 0  # Current time at any point in the experiment
        self.upf_dict = {}  # UPF dictionary

    def schedule_event(self, event):
        heapq.heappush(self.events, event)

    def next_event(self):
        if self.events:
            return heapq.heappop(self.events)
        else:
            return None

    def run_simulation(self):

        while self.current_time <= self.total_simulation_time:
            event = self.next_event()
            if event is None:
                break

            self.current_time = int(event.event_time)  # Convert current_time to integer
            self.current_time = min(self.current_time,
                                    self.total_simulation_time)  # Ensure current_time does not exceed bounds

            if event.event_type == Events.UE_init:
                for ue in self.ue_list:
                    ue.generate_pdu_session()
                    ue.pdu_session_generation(self)
            elif event.event_type == Events.PDU_request:
                pdu_session = event.obj
                if pdu_session not in self.upf_dict:
                    self.upf_dict[pdu_session] = UPF(f"UPF{len(self.upf_dict)}", 0, self.current_time, 3)
                upf = self.upf_dict[pdu_session]
                self.compute_node.allocate_upf(pdu_session, self.current_time)  # Removed 'upf' argument
            elif event.event_type == Events.PDU_terminate:
                pdu_session = event.obj
                upf = self.upf_dict[pdu_session]
                upf.terminate_pdu_session(pdu_session, self)
                upf_terminate_event = Event(self.current_time + 1, Events.UPF_terminate, 4, upf)
                self.schedule_event(upf_terminate_event)
            elif event.event_type == Events.PDU_session_generation:
                for ue in self.ue_list:
                    ue.generate_pdu_session()

        # After all events have been processed, check if there are remaining PDUs
        additional_pdu = [event.obj for event in self.events if event.event_type == Events.PDU_request]
        if not additional_pdu:
            # If there are no remaining PDUs, create a new UPF to handle them
            last_event_time = max(event.event_time for event in self.events) if self.events else 0
            last_pdu_time = max(
                (event.obj.event_time for event in self.events if event.event_type == Events.PDU_request), default=0)
            last_event_time = max(last_event_time, last_pdu_time)
            self.compute_node.allocate_upf("additional PDU", last_event_time)

