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

    def terminate_pdu(self, simulation_clock, event_manager):
        with open("output.txt", "a") as file:
            print(f"{simulation_clock:.2f}: {self.generate_pdu_id()} terminated after processing", file=file)

    def __str__(self):
        if self.start_time is not None:
            return (
                f"{self.start_time:.2f}: {self.generate_pdu_id()} - {self.pdu_data} (Duration: {self.duration} seconds)"
            )
        else:
            return f"{self.generate_pdu_id()} - {self.pdu_data} (Duration: {self.duration} seconds)"
