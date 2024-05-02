import heapq
from events import Events
from upf import UPF


class Scheduler:

    def __init__(self, total_simulation_time, max_upfs, t, csv_writer):
        self.compute_node = None  # Compute Node in experiment
        self.ue_list = []  # List of UEs
        self.events = []  # List of events
        self.total_simulation_time = total_simulation_time  # Total simulation time for the experiment
        self.current_time = 0  # Current time at any point in the experiment
        self.upf_dict = {}  # UPF dictionary
        self.max_upfs = max_upfs  # Maximum number of UPFs allowed during simulation
        self.t = t  # Maximum slots in a UPF
        self.csv_writer = csv_writer  # Storing output in csv file

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
            self.current_time = min(self.current_time, self.total_simulation_time)  # Ensure current_time does not
            # exceed bounds

            if event.event_type == Events.UE_init:
                for ue in self.ue_list:
                    ue.generate_pdu_session()
                    ue.pdu_session_generation(self, self.csv_writer)
            elif event.event_type == Events.PDU_request:
                pdu_session = event.obj
                if pdu_session not in self.upf_dict:
                    self.upf_dict[pdu_session] = UPF(f"UPF{len(self.upf_dict)}", 0, self.current_time, self.t, self.csv_writer)
                upf = self.upf_dict[pdu_session]
                self.compute_node.allocate_upf(pdu_session, self.current_time)
            elif event.event_type == Events.PDU_terminate:
                pdu_session = event.obj
                upf = self.upf_dict[pdu_session]
                upf.terminate_pdu_session(pdu_session, self)
