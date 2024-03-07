class ComputeNode:
    def __init__(self, name, scheduler, node_id, cpu_capacity, storage_capacity):
        self.name = name
        self.scheduler = scheduler
        self.node_id = node_id
        self.cpu_capacity = cpu_capacity
        self.storage_capacity = storage_capacity
        self.list_upf = []

    def allocate_upf(self, pdu_session, upf, current_time):
        print(f"Simulation Clock: {current_time}, "
              f"Compute Node {self.name} allocated UPF {upf.name} for processing PDU session {pdu_session}")
        upf.process_pdu_session(pdu_session, current_time, self.scheduler)
