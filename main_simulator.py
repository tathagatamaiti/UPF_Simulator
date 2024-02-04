from ue import UE
from compute_node import ComputeNode
from event_manager import EventManager


def initialize_simulation(total_simulation_time):
    # Create instances of ComputeNode, multiple UEs, and EventManager
    event_manager = EventManager()
    compute_node = ComputeNode(event_manager)

    # Number of UEs
    num_ues = 2
    ues = [UE(compute_node, total_simulation_time, event_manager, ue_id=i + 1) for i in range(num_ues)]

    # Register UEs with the ComputeNode
    for ue in ues:
        compute_node.add_upf(ue)

    return event_manager, compute_node, ues


def run_simulation(event_manager, compute_node, ues):
    simulation_clock = 0
    while any(ue.generate_pdu_sessions(simulation_clock, event_manager) for ue in
              ues) and simulation_clock <= total_simulation_time:
        pass

    # Process events
    event_manager.process_events()

    print("Simulation completed. Output written to output.txt")


if __name__ == "__main__":
    total_simulation_time = 30
    event_manager, compute_node, ues = initialize_simulation(total_simulation_time)
    run_simulation(event_manager, compute_node, ues)
