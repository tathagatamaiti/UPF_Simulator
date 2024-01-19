from queue import Queue
import time


class PDU:
    def __init__(self, ue_id, pdu_data, counter, duration):
        self.ue_id = ue_id
        self.pdu_data = pdu_data
        self.counter = counter
        self.duration = duration
        self.start_time = None
        self.upf = None

    def generate_pdu_id(self):
        return f"PDU_{self.ue_id}_{self.counter}"

    def associate_upf(self, upf):
        self.upf = upf

    def terminate_pdu(self):
        # Simulate termination delay
        time.sleep(1)
        with open("output.txt", "a") as file:
            print(f"{self.generate_pdu_id()} terminated after processing", file=file)

    def __str__(self):
        return f"{self.generate_pdu_id()}: {self.pdu_data} (Duration: {self.duration} seconds)"


class UE:
    def __init__(self, compute_node, threshold, pdu_limit):
        self.ue_id = 1
        self.compute_node = compute_node
        self.threshold = threshold
        self.pdu_counter = 0
        self.pdu_limit = pdu_limit
        self.pdu_queue = Queue()

    def generate_pdu_sessions(self):
        for _ in range(self.threshold - 1):
            pdu_data = f"PDU data for UE"
            pdu_duration = 5  # Set the duration for each PDU session in seconds
            pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter, pdu_duration)
            self.pdu_queue.put(pdu_session)
            with open("output.txt", "a") as file:
                print(f"Generated {pdu_session}", file=file)

            self.pdu_counter += 1

        # Generate a PDU session with longer duration 200 seconds
        pdu_data = f"Long-duration PDU data for UE"
        pdu_duration = 200
        pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter, pdu_duration)
        self.pdu_queue.put(pdu_session)
        with open("output.txt", "a") as file:
            print(f"Generated {pdu_session}", file=file)

        # Send PDU request message for the generated PDU sessions
        with open("output.txt", "a") as file:
            print(f"UE{self.ue_id} sending PDU requests to Compute Node at time {time.time()}", file=file)
        self.compute_node.process_pdu_requests(self)

        return self.pdu_counter < self.pdu_limit


class UPF:
    def __init__(self, upf_id):
        self.upf_id = upf_id
        self.start_time = None

    def process_pdu(self, pdu_session):
        pdu_session.start_time = time.time()  # Simulating a delay before processing starts
        pdu_session.associate_upf(self)
        with open("output.txt", "a") as file:
            print(f"{self.upf_id} processing {pdu_session}", file=file)

        # Simulate processing time
        time.sleep(1)
        with open("output.txt", "a") as file:
            print(f"{self.upf_id} completed processing {pdu_session}", file=file)

        pdu_session.terminate_pdu()


class ComputeNode:
    def __init__(self):
        self.upfs = []

    def add_upf(self, upf):
        self.upfs.append(upf)

    def generate_upf(self, pdu_session):
        new_upf_id = f"UPF_{pdu_session.generate_pdu_id()}"
        new_upf = UPF(new_upf_id)
        self.add_upf(new_upf)
        return new_upf

    def process_pdu_requests(self, ue):
        with open("output.txt", "a") as file:
            print(f"Compute Node processing PDU requests at time {time.time()}", file=file)
        while not ue.pdu_queue.empty():
            pdu_session = ue.pdu_queue.get()
            # Generate a new UPF for each PDU session
            new_upf = self.generate_upf(pdu_session)
            with open("output.txt", "a") as file:
                print(f"{new_upf.upf_id} assigned to process {pdu_session}", file=file)
            new_upf.process_pdu(pdu_session)


# Set the threshold for PDU session generation and processing
threshold = 3
pdu_limit = 20

# Create instances of ComputeNode and UE
compute_node = ComputeNode()
ue = UE(compute_node, threshold, pdu_limit)

# Register UE with the ComputeNode
compute_node.add_upf(ue)

# Generate and process PDUs until the pdu_limit is reached
while ue.generate_pdu_sessions():
    pass

print("Simulation completed. Output written to output.txt.")
