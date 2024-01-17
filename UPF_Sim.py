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
    def __init__(self, ue_id, threshold):
        self.ue_id = ue_id
        self.threshold = threshold
        self.pdu_counter = 0
        self.pdu_queue = Queue()

    def generate_pdu_session(self):
        pdu_data = f"PDU data for UE_{self.ue_id}"
        pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter)
        self.pdu_queue.put(pdu_session)
        with open("output.txt", "a") as file:
            print(f"{self.ue_id} generated {pdu_session} and added it to the queue.", file=file)

        self.pdu_counter += 1

        if self.pdu_queue.qsize() >= self.threshold:
            timestamp = time.strftime('%Y%m%d%H%M%S')
            new_upf_id = f"UPF_{self.ue_id}_{timestamp}"
            new_upf = UPF(new_upf_id)
            new_upf.process_pdu_sessions(self.pdu_queue)


class UPF:
    def __init__(self, upf_id):
        self.upf_id = upf_id
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    def process_pdu_sessions(self, pdu_queue):
        while not pdu_queue.empty():
            pdu_session = pdu_queue.get()
            with open("output.txt", "a") as file:
                print(f"{self.upf_id} ({self.timestamp}) processing {pdu_session}", file=file)


time_interval = 1

ue1 = UE("UE1", threshold=3)
ue2 = UE("UE2", threshold=2)

schedule.every(time_interval).seconds.do(ue1.generate_pdu_session)
schedule.every(time_interval).seconds.do(ue2.generate_pdu_session)

start_time = time.time()
while time.time() - start_time < 60:
    schedule.run_pending()

print("Simulation completed. Output written to output.txt.")
