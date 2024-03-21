import heapq
from event import Event
from upf import UPF


class Scheduler:
    def __init__(self, total_simulation_time):
        self.compute_node = None  # Compute Node in experiment
        self.ue_list = []  # List of UEs
        self.events = []  # List of events
        self.total_simulation_time = total_simulation_time  # Total simulation time for the experiment
        self.current_time = 0  # Current time at any point in the experiment
        self.upf_dict = {}  # UPF dictionary
        self.pdu_upf_map = {}  # Mapping from PDU sessions to corresponding UPFs

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

            self.current_time = event.event_time
            if event.event_type == 'UE_init':
                for ue in self.ue_list:
                    ue.generate_pdu_session()
                    ue.pdu_session_generation(self)
            elif event.event_type == 'PDU_request':
                pdu_session = event.obj
                if pdu_session not in self.pdu_upf_map:
                    self.pdu_upf_map[pdu_session] = UPF(f"UPF{len(self.upf_dict)}", 0, 0, 20)
                upf = self.pdu_upf_map[pdu_session]
                self.compute_node.allocate_upf(pdu_session, upf, self.current_time)
            elif event.event_type == 'PDU_terminate':
                pdu_session = event.obj
                upf = self.pdu_upf_map.get(pdu_session)
                if upf is None:
                    # Handle error or skip event if UPF not found
                    continue
                upf.terminate_pdu_session(pdu_session, event.termination_type, self)
            elif event.event_type == 'PDU_session_generation':
                for ue in self.ue_list:
                    ue.generate_pdu_session()
            elif event.event_type == 'UPF_terminate':
                event.obj.terminate(self)
