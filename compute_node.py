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
        if self.list_upf:
            # Find the UPF with the lowest number of assigned PDUs
            best_upf = min(self.list_upf, key=lambda upf: upf.num_pdus_handled)
            if best_upf.can_handle_more_pdus():
                best_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
            else:
                # If the UPF with the lowest number of assigned PDUs cannot handle more PDUs, create a new one
                upf_name = f"UPF{len(self.list_upf)}"
                new_upf = UPF(upf_name, len(self.list_upf), current_time, self.maxnum_pdu)
                self.list_upf.append(new_upf)
                new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
        else:
            # If there are no existing UPFs, create a new one to handle the PDU
            upf_name = f"UPF0"
            new_upf = UPF(upf_name, 0, current_time, self.maxnum_pdu)
            self.list_upf.append(new_upf)
            new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
