from ue import UE
from compute_node import ComputeNode
from events import EventManager


def main():
    threshold = 5
    pdu_limit = 100

    event_manager = EventManager()

    compute_node = ComputeNode(event_manager)
    ue = UE(compute_node, threshold, pdu_limit, event_manager)

    compute_node.add_upf(ue)

    simulation_clock = 0
    while ue.generate_pdu_sessions(simulation_clock):
        # Process events scheduled at the current simulation clock
        events_at_current_time = [event for event in event_manager.events if event[0] == simulation_clock]
        for event in events_at_current_time:
            print(f"{event[0]:.2f}: {event[1]}")

        # Update the simulation clock to the next time
        simulation_clock += 1

    event_manager.write_events_to_file("output.txt")
    print("Simulation completed. Output written to output.txt.")


if __name__ == "__main__":
    main()
