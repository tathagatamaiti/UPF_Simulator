import random


class PDU:
    def __init__(self, pdu_id, pdu_class, source_ue, compute_node, pdu_start_time):
        self.pdu_id = pdu_id
        self.pdu_class = pdu_class
        self.source_ue = source_ue
        self.compute_node = compute_node
        self.assigned_upf = None
        self.pdu_start_time = pdu_start_time
        self.pdu_duration = random.randint(5, 10)
