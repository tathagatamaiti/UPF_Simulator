class PDU:
    def __init__(self, pdu_id, pdu_class, source_ue, compute_node, pdu_start_time, pdu_duration):
        self.pdu_id = pdu_id  # PDU id
        self.pdu_class = pdu_class  # Class of PDU being generated
        self.source_ue = source_ue  # Source UE of PDU being generated
        self.compute_node = compute_node  # Compute node handling PDU
        self.assigned_upf = None  # UPF being assigned to PDU
        self.pdu_start_time = pdu_start_time  # Start time of the PDU
        self.pdu_duration = pdu_duration  # Duration of the PDU
