from ue import UE
from compute_node import ComputeNode
from event_manager import EventManager


def initialize_simulation(total_simulation_time):
    event_manager = EventManager()
    compute_node = ComputeNode(event_manager)
    ue = UE(compute_node, event_manager)
    event_manager.schedule_event(ue.initialize_event())
    return event_manager


def run_simulation(event_manager, total_simulation_time):
    event_manager.process_events(total_simulation_time)


if __name__ == "__main__":
    total_simulation_time = 20
    event_manager = initialize_simulation(total_simulation_time)
    run_simulation(event_manager, total_simulation_time)
