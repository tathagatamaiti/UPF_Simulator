from upf import UPF


class ComputeNode:
    def __init__(self, name, scheduler, node_id, cpu_capacity, storage_capacity, maxnum_pdu):
        self.name = name
        self.scheduler = scheduler  # Scheduler of the experiment
        self.node_id = node_id  # Compute Node id
        self.cpu_capacity = cpu_capacity  # CPU capacity at Compute Node
        self.storage_capacity = storage_capacity  # Storage capacity of Compute Node
        self.upf_instances = {}  # Dictionary to store UPF instances
        self.upf_counter = 0  # Counter to generate unique UPF names
        self.maxnum_pdu = maxnum_pdu  # Maximum number of PDUs that can be handled by the UPF

    def allocate_upf(self, pdu_session, current_time):
        if self.upf_instances:
            # Find the UPF with the lowest number of assigned PDUs
            best_upf_id = min(self.upf_instances, key=lambda upf_id: self.upf_instances[upf_id].num_pdus_handled)
            best_upf = self.upf_instances[best_upf_id]

            if best_upf.can_handle_more_pdus():
                best_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
            else:
                # If the UPF with the lowest number of assigned PDUs cannot handle more PDUs, create a new one
                new_upf_name = f"UPF{self.upf_counter}"
                new_upf = UPF(new_upf_name, self.upf_counter, current_time, self.maxnum_pdu)
                self.upf_instances[self.upf_counter] = new_upf
                self.upf_counter += 1
                new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
        else:
            # If there are no existing UPFs, create a new one to handle the PDU
            new_upf_name = f"UPF0"
            new_upf = UPF(new_upf_name, 0, current_time, self.maxnum_pdu)
            self.upf_instances[0] = new_upf
            self.upf_counter += 1
            new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
