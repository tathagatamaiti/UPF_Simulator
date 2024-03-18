from upf import UPF


class ComputeNode:

    # DEFINING EXPERIMENT PARAMETERS

    maxnum_pdu = "MAXIMUM NUMBER OF PDUs IN THE EXPERIMENT"
    node_id = "COMPUTE NODE ID"
    cpu_capacity = "CPU CAPACITY AT COMPUTE NODE"
    storage_capacity = "STORAGE CAPACITY OF COMPUTE NODE"

    def __init__(self, name, scheduler, node_id, cpu_capacity, storage_capacity, maxnum_pdu):
        self.name = name
        self.scheduler = scheduler
        self.node_id = node_id
        self.cpu_capacity = cpu_capacity
        self.storage_capacity = storage_capacity
        self.list_upf = []
        self.maxnum_pdu = maxnum_pdu

        for i in range(maxnum_pdu):
            upf_name = f"{self.name}_UPF{i}"
            upf = UPF(upf_name, self.scheduler, 0, 20)
            self.list_upf.append(upf)

    def allocate_upf(self, pdu_session, upf, current_time):
        print(f"Simulation Clock: {current_time}, "
              f"Compute Node {self.name} allocated UPF {upf.name} for processing PDU session {pdu_session}")
        upf.process_pdu_session(pdu_session, current_time, self.scheduler)
