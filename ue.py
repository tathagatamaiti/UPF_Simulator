import random
from queue import Queue
from pdu import PDU


class UE:
    def __init__(self, compute_node, threshold, pdu_limit, event_manager):
        self.ue_id = 1
        self.compute_node = compute_node
        self.threshold = threshold
        self.pdu_counter = 0
        self.pdu_limit = pdu_limit
        self.pdu_queue = Queue()
        self.event_manager = event_manager

    def generate_pdu_sessions(self, simulation_clock):
        while self.pdu_counter < self.pdu_limit:
            pdu_data = f"PDU data for UE"
            pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter)
            pdu_session.start_time = simulation_clock
            self.pdu_queue.put(pdu_session)

            self.event_manager.schedule_event(simulation_clock, f"UE{self.ue_id} generated {pdu_session}")
            self.pdu_counter += 1

            if self.pdu_counter % self.threshold == 0 or self.pdu_counter == self.pdu_limit:
                # Send PDU requests to Compute Node only when the threshold is reached or all PDUs are generated
                self.event_manager.schedule_event(simulation_clock,
                                                  f"UE{self.ue_id} sending PDU requests to Compute Node")
                self.compute_node.process_pdu_requests(self, simulation_clock)

            # Introduce a random delay between the creation of PDU sessions
            delay = random.uniform(1.0, 5.0)
            simulation_clock += delay

        return False
