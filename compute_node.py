import numpy as np
from event import Event
from events import Events
from upf import UPF


class ComputeNode:
    def __init__(self, name, scheduler, node_id, cpu_capacity, storage_capacity, max_upfs, t, csv_writer, T1, T2, M):
        self.name = name
        self.scheduler = scheduler
        self.node_id = node_id
        self.cpu_capacity = cpu_capacity
        self.storage_capacity = storage_capacity
        self.upf_instances = {}
        self.upf_counter = 0
        self.max_upfs = max_upfs
        self.t = t
        self.csv_writer = csv_writer
        self.T1 = T1  # Threshold for scaling out
        self.T2 = T2  # Threshold for scaling in
        self.M = M
        self.J = len(self.upf_instances)

    def allocate_upf(self, pdu_session, current_time):
        if self.upf_instances:
            # Find the UPF with the lowest number of assigned PDUs
            best_upf_id = min(self.upf_instances, key=lambda upf_id: self.upf_instances[upf_id].num_pdus_handled)
            best_upf = self.upf_instances[best_upf_id]

            if best_upf.can_handle_more_pdus():
                best_upf.process_pdu_session(pdu_session, current_time, self.scheduler)
            else:
                self.scale_out(pdu_session, current_time)
                self.scale_in(current_time)
        else:
            # If there are no existing UPFs, create a new one to handle the PDU
            self.scale_out(pdu_session, current_time)

        self.csv_writer.writerow([current_time, pdu_session, ""])  # Write data to CSV

    def scale_out(self, pdu_session, current_time):
        if self.J < self.max_upfs:
            new_upf_name = f"UPF{self.upf_counter}"
            new_upf = UPF(new_upf_name, self.upf_counter, current_time, self.t, self.csv_writer)
            self.upf_instances[new_upf_name] = new_upf
            self.upf_counter += 1
            new_upf.process_pdu_session(pdu_session, current_time, self.scheduler)

    def scale_in(self, current_time):
        for upf_name, upf_instance in list(self.upf_instances.items()):
            if upf_instance.num_pdus_handled == 0:
                if self.J > self.M:
                    # Initiate scaling-in action
                    self.terminate_upf(upf_instance, current_time)
                    break  # Only terminate one UPF instance at a time

    def terminate_upf(self, upf_instance, current_time):
        termination_event = Event(current_time, Events.UPF_terminate, 4, upf_instance)
        self.scheduler.schedule_event(termination_event)
        print(f"{Event.event_id_counter}, {np.ceil(self.scheduler.current_time)}, "
              f"{upf_instance.name} terminated")
        del self.upf_instances[upf_instance.name]
