import numpy as np

from upf import UPF


class ComputeNode:

    def __init__(self, name, scheduler, node_id, cpu_capacity, storage_capacity, maxnum_pdu):
        self.name = name
        self.scheduler = scheduler  # Scheduler of the experiment
        self.node_id = node_id  # Compute Node id
        self.cpu_capacity = cpu_capacity  # CPU capacity at Compute Node
        self.storage_capacity = storage_capacity  # Storage capacity of Compute Node
        self.list_upf = []  # List of UPFs
        self.maxnum_pdu = maxnum_pdu  # Maximum number of PDUs that can be handled by the UPF

        for i in range(maxnum_pdu):
            upf_name = f"{self.name}_UPF{i}"
            upf = UPF(upf_name, self.scheduler, 0, 3)
            self.list_upf.append(upf)

    def allocate_upf(self, pdu_session, upf, current_time):
        print(f"{np.ceil(current_time)}, "
              f"{self.name} allocated {upf.name} for processing {pdu_session}")
        upf.process_pdu_session(pdu_session, current_time, self.scheduler)
