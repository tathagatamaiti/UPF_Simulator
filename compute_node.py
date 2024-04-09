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

    def allocate_upf(self, pdu_session, current_time):
        for upf in self.list_upf:
            if upf.can_handle_more_pdus():
                upf.process_pdu_session(pdu_session, current_time, self.scheduler)
                return

        # If no existing UPF can handle more PDUs, create a new one
        upf_name = f"{self.name}_UPF{len(self.list_upf)}"
        new_upf = UPF(upf_name, len(self.list_upf), current_time, self.maxnum_pdu)
        self.list_upf.append(new_upf)
        new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
