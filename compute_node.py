import numpy as np

from event import Event
from events import Events
from upf import UPF


class ComputeNode:
    def __init__(self, name, scheduler, node_id, cpu_capacity, storage_capacity, max_upfs, t, csv_writer):
        self.name = name
        self.scheduler = scheduler  # Scheduler of the experiment
        self.node_id = node_id  # Compute Node id
        self.cpu_capacity = cpu_capacity  # CPU capacity at Compute Node
        self.storage_capacity = storage_capacity  # Storage capacity of Compute Node
        self.upf_instances = {}  # Dictionary to store UPF instances
        self.upf_counter = 0  # Counter to generate unique UPF names
        self.max_upfs = max_upfs  # Maximum number of UPFs allowed during simulation
        self.T = t  # Maximum slots in a UPF
        self.csv_writer = csv_writer

    def allocate_upf(self, pdu_session, current_time):
        if self.upf_instances:
            # Find the UPF with the lowest number of assigned PDUs
            best_upf_id = min(self.upf_instances, key=lambda upf_id: self.upf_instances[upf_id].num_pdus_handled)
            best_upf = self.upf_instances[best_upf_id]

            if best_upf.can_handle_more_pdus():
                best_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
            else:
                # If the UPF with the lowest number of assigned PDUs cannot handle more PDUs, create a new one
                self.scale_out(pdu_session, current_time)
        else:
            # If there are no existing UPFs, create a new one to handle the PDU
            self.scale_out(pdu_session, current_time)

        self.csv_writer.writerow([current_time, pdu_session, ""])  # Write data to CSV

    def scale_out(self, pdu_session, current_time):
        if len(self.upf_instances) < self.max_upfs:
            new_upf_name = f"UPF{self.upf_counter}"
            new_upf = UPF(new_upf_name, self.upf_counter, current_time, self.T, self.csv_writer)
            self.upf_instances[new_upf_name] = new_upf
            self.upf_counter += 1
            new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)

    def scale_in(self, current_time, scheduler):
        for upf_name, upf_instance in list(self.upf_instances.items()):
            if upf_instance.num_pdus_handled == 0:
                termination_event = Event(current_time, Events.UPF_terminate, 4, upf_name)
                scheduler.schedule_event(termination_event)
                print(f"{Event.event_id_counter}, {np.ceil(self.scheduler.current_time)}, "
                      f"{upf_name} terminated")
                del self.upf_instances[upf_name]
