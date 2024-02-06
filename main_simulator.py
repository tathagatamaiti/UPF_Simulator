from ue import UE
from compute_node import ComputeNode
from event_manager import EventManager


def initialize_simulation():
    # Create instances of ComputeNode, multiple UEs, and EventManager
    event_manager = EventManager()
    compute_node = ComputeNode(event_manager)

    # Number of UEs
    num_ues = 2
    ues = [UE(compute_node, event_manager, ue_id=i + 1) for i in range(num_ues)]

    # Register UEs with the ComputeNode
    for ue in ues:
        compute_node.add_upf(ue)

    return event_manager, compute_node, ues


def run_simulation(event_manager, compute_node, total_simulation_time):
    while event_manager.has_events():
        event = event_manager.next_event()
        event_type = event.get_type()

        if event_type == "UE_INITIALIZATION":
            # UE Initialization event
            for ue in event_manager.get_objects("UE"):
                ue.generate_pdu_sessions(event.get_time(), event_manager)

        elif event_type == "UE_GENERATE_PDU_SESSION":
            ue = event_manager.get_object(event.get_description())
            ue.generate_pdu_sessions(event.get_time(), event_manager)

        elif event_type == "COMPUTE_NODE_ALLOCATE_UPF":
            ue = event_manager.get_object(event.get_description())
            compute_node.process_pdu_requests(ue, event.get_time(), event_manager)

        elif event_type == "UPF_PROCESS_PDU":
            upf = event_manager.get_object(event.get_description())
            upf.process_next_pdu(event_manager, event.get_time())

        elif event_type == "PDU_SESSION_TERMINATE":
            pdu_session = event_manager.get_object(event.get_description())
            pdu_session.terminate(event_manager, event.get_time())

        elif event_type == "UPF_TERMINATE":
            upf = event_manager.get_object(event.get_description())
            upf.terminate(event_manager, event.get_time())

    print("Simulation completed. Output written to output.txt")


if __name__ == "__main__":
    event_manager, compute_node, ues = initialize_simulation()
    total_simulation_time = 20
    # Schedule UE Initialization event
    init_event = event_manager.create_event(0, "UE_INITIALIZATION", "UE Initialization")
    event_manager.schedule_event(init_event)

    run_simulation(event_manager, compute_node, total_simulation_time)
