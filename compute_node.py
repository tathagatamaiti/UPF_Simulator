class ComputeNode:
    def __init__(self, name, scheduler):
        self.name = name
        self.scheduler = scheduler

    def allocate_upf(self, pdu_session, upf, current_time):
        print(f"Simulation Clock: {current_time}, "
              f"Compute Node {self.name} allocated UPF {upf.name} for processing PDU session {pdu_session}")
        upf.process_pdu_session(pdu_session, current_time, self.scheduler)
