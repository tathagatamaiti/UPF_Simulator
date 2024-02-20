from event import Event


class UE:
    def __init__(self, name):
        self.name = name
        self.next_pdu_session_id = 0

    def generate_pdu_session(self):
        pdu_session = f"{self.name}_pdu{self.next_pdu_session_id}"
        self.next_pdu_session_id += 1
        return pdu_session

    def send_pdu_request(self, pdu_session, compute_node, scheduler):
        print(f"Simulation Clock: {scheduler.current_time}, "
              f"UE {self.name} sends PDU request to Compute Node {compute_node.name} for PDU session {pdu_session}")
        pdu_request_event = Event(scheduler.current_time + 1, 'PDU_request', pdu_session)
        scheduler.schedule_event(pdu_request_event)
        print(f"Simulation Clock: {scheduler.current_time}, UE {self.name} generated PDU session {pdu_session}")
