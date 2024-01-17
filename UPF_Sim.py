import schedule
import time
from queue import Queue


class PDU:
    def __init__(self, ue_id, pdu_data, counter):
        self.ue_id = ue_id
        self.pdu_data = pdu_data
        self.counter = counter

    def generate_pdu_id(self):
        return f"PDU_{self.ue_id}_{self.counter}"

    def __str__(self):
        return f"{self.generate_pdu_id()}: {self.pdu_data}"


class UE:
    def __init__(self, ue_id, compute_node, threshold):
        self.ue_id = ue_id
        self.threshold = threshold
        self.pdu_counter = 0
        self.compute_node = compute_node

    def generate_pdu_sessions(self):
        pdu_data = f"PDU data for UE_{self.ue_id}"
        for _ in range(self.threshold):
            pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter)
            self.compute_node.process_pdu_request(self, pdu_session)
            self.pdu_counter += 1


class UPF:
    def __init__(self, upf_id):
        self.upf_id = upf_id
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')


class ComputeNode:
    def __init__(self):
        self.ues = []
        self.upfs = []

    def add_ue(self, ue):
        self.ues.append(ue)

    def add_upf(self, upf):
        self.upfs.append(upf)

    def generate_upf(self, ue_id):
        timestamp = time.strftime('%Y%m%d%H%M%S')
        new_upf_id = f"UPF_{ue_id}_{timestamp}"
        new_upf = UPF(new_upf_id)
        self.add_upf(new_upf)
        return new_upf

    def process_pdu_request(self, ue, pdu_session):
        with open("output.txt", "a") as file:
            print(f"{ue.ue_id} generated {pdu_session} and sent request to ComputeNode.", file=file)

        # Ensure there is at least one UPF available
        if len(self.upfs) == 0:
            new_upf = self.generate_upf(ue.ue_id)
            with open("output.txt", "a") as file:
                print(f"No available UPFs. Generated {new_upf.upf_id} to process {pdu_session}.", file=file)

        # Assign the PDU session to an available UPF with the corresponding UE's ID
        upf = next((upf for upf in self.upfs if ue.ue_id in upf.upf_id), None)
        if upf:
            with open("output.txt", "a") as file:
                print(f"{upf.upf_id} ({upf.timestamp}) processing {pdu_session}", file=file)
        else:
            with open("output.txt", "a") as file:
                print(f"No available UPFs for {ue.ue_id}.", file=file)


# Set the time interval for PDU session generation in seconds
time_interval = 1

# Create instances of ComputeNode, UEs, and UPFs
compute_node = ComputeNode()
ue1 = UE("UE1", compute_node, threshold=3)
ue2 = UE("UE2", compute_node, threshold=2)

# Register UEs with the ComputeNode
compute_node.add_ue(ue1)
compute_node.add_ue(ue2)

# Generate initial UPFs
compute_node.generate_upf(ue1.ue_id)
compute_node.generate_upf(ue2.ue_id)

# Schedule the PDU session generation function for both UEs
schedule.every(time_interval).seconds.do(ue1.generate_pdu_sessions)
schedule.every(time_interval).seconds.do(ue2.generate_pdu_sessions)

# Run the scheduler for 60 seconds
start_time = time.time()
while time.time() - start_time < 60:
    schedule.run_pending()

# Log completion message to the console
print("Simulation completed. Output written to output.txt.")
