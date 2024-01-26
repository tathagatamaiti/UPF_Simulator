import random
from pdu import PDU


class UE:
    def __init__(self, compute_node, threshold, pdu_limit):
        self.ue_id = 1
        self.compute_node = compute_node
        self.threshold = threshold
        self.pdu_counter = 0
        self.pdu_limit = pdu_limit
        self.pdu_queue = []

    def generate_pdu_sessions(self, simulation_clock, event_manager):
        for _ in range(self.threshold - 1):
            pdu_data = f"PDU data for UE"
            pdu_duration = 5
            pdu_session = PDU(self.ue_id, pdu_data, self.pdu_counter, pdu_duration)
            pdu_session.start_time = simulation_clock
            description = f"UE{self.ue_id} generated {pdu_session}"
            event_manager.schedule_event(simulation_clock, description)

            self.pdu_counter += 1

            # Introduce a random delay between the creation of PDU sessions
            delay = random.uniform(1.0, 5.0)
            simulation_clock += delay

            # Add the generated PDU session to the queue
            self.pdu_queue.append(pdu_session)

        # Send PDU request message for the generated PDU sessions
        description = f"UE{self.ue_id} sending PDU requests to Compute Node"
        event_manager.schedule_event(simulation_clock, description)
        self.compute_node.process_pdu_requests(self, simulation_clock, event_manager)

        return self.pdu_counter < self.pdu_limit
