import heapq
import random


class Event:
    def __init__(self, time, event_type, obj=None):
        self.time = time
        self.event_type = event_type
        self.obj = obj

    def __lt__(self, other):
        return self.time < other.time


class UE:
    def __init__(self, name):
        self.name = name
        self.next_pdu_session_id = 0

    def generate_pdu_session(self):
        pdu_session = f"{self.name}_pdu{self.next_pdu_session_id}"
        self.next_pdu_session_id += 1
        return pdu_session

    def send_pdu_request(self, pdu_session, compute_node, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, "
              f"UE {self.name} sends PDU request to Compute Node {compute_node.name} for PDU session {pdu_session}")
        pdu_request_event = Event(scheduler.current_time + 1, 'PDU_request', pdu_session)
        scheduler.schedule_event(pdu_request_event)
        print(f"Simulation Clock: {scheduler.current_time}, UE {self.name} generated PDU session {pdu_session}")


class ComputeNode:
    def __init__(self, name, scheduler):
        self.name = name
        self.scheduler = scheduler

    def allocate_upf(self, pdu_session, upf, current_time):
        print(f"Simulation Clock: {current_time}, "
              f"Compute Node {self.name} allocated UPF {upf.name} for processing PDU session {pdu_session}")
        upf.process_pdu_session(pdu_session, current_time, self.scheduler)


class UPF:
    def __init__(self, name):
        self.name = name

    def process_pdu_session(self, pdu_session, current_time, scheduler):
        print(f"Simulation Clock: {current_time}, UPF {self.name} processing PDU session {pdu_session}")
        termination_time = random.randint(5, 10)
        termination_event = Event(current_time + termination_time, 'PDU_terminate', pdu_session)
        scheduler.schedule_event(termination_event)

    def terminate_pdu_session(self, pdu_session, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, PDU session {pdu_session} terminated")
        print(
            f"Simulation Clock: {scheduler.current_time}, UPF {self.name} terminated processing PDU session {pdu_session}")

    def terminate(self, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, UPF {self.name} terminated")


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
            self.current_time = event.time
            if event.event_type == 'UE_init':
                for ue in self.ue_list:
                    pdu_session = ue.generate_pdu_session()
                    ue.send_pdu_request(pdu_session, self.compute_node, self)
            elif event.event_type == 'PDU_request':
                pdu_session = event.obj
                if pdu_session not in self.upf_dict:
                    self.upf_dict[pdu_session] = UPF(f"UPF{len(self.upf_dict)}")
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


def main():
    total_simulation_time = 10
    ue_list = [UE(f"UE{i}") for i in range(3)]
    scheduler = Scheduler(total_simulation_time)
    compute_node = ComputeNode("CN0", scheduler)

    scheduler.ue_list = ue_list
    scheduler.compute_node = compute_node

    for ue in ue_list:
        init_event = Event(0, 'UE_init', ue)
        scheduler.schedule_event(init_event)

    scheduler.run_simulation()


if __name__ == "__main__":
    main()
