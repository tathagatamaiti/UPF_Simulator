class PDU:
    def __init__(self, pdu_data, duration):
        self.pdu_data = pdu_data
        self.duration = duration
        self.start_time = None

    def generate_pdu_id(self):
        return f"PDU_{id(self)}"

    def __str__(self):
        if self.start_time is not None:
            return f"{self.generate_pdu_id()} - {self.pdu_data} (Duration: {self.duration} seconds)"
        else:
            return f"{self.generate_pdu_id()} - {self.pdu_data} (Duration: {self.duration} seconds)"
