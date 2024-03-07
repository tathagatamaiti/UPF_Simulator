import heapq
from upf import UPF
from event import Event


class Scheduler:
    def __init__(self, total_simulation_time):
        self.events = []
        self.total_simulation_time = total_simulation_time
        self.current_time = 0
        self.upf_dict = {}

    def schedule_event(self, event):
        heapq.heappush(self.events, event)

    def run_simulation(self):
        while self.current_time <= self.total_simulation_time:
            if not self.events:
                break

            event = heapq.heappop(self.events)
            self.current_time = event.event_time
            if event.event_type == 'UE_init':
                for ue in self.ue_list:
                    pdu_session = ue.generate_pdu_session()
                    ue.send_pdu_request(pdu_session, self.compute_node, self)
            elif event.event_type == 'PDU_request':
                pdu_session = event.obj
                if pdu_session not in self.upf_dict:
                    self.upf_dict[pdu_session] = UPF(f"UPF{len(self.upf_dict)}", 0, 0, 0)
                upf = self.upf_dict[pdu_session]
                self.compute_node.allocate_upf(pdu_session, upf, self.current_time)
            elif event.event_type == 'PDU_terminate':
                pdu_session = event.obj
                upf = self.upf_dict[pdu_session]
                upf.terminate_pdu_session(pdu_session, self)
                upf_terminate_event = Event(self.current_time + 1, 'UPF_terminate', upf)
                self.schedule_event(upf_terminate_event)
            elif event.event_type == 'UPF_terminate':
                event.obj.terminate(self)
