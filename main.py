from event import Event
from ue import UE
from compute_node import ComputeNode
from scheduler import Scheduler


def main():
    scheduler = Scheduler(total_simulation_time=10)
    ue_list = [UE(f"UE{i}") for i in range(3)]
    compute_node = ComputeNode("CN0", scheduler)
    scheduler.ue_list = ue_list
    scheduler.compute_node = compute_node

    initial_events = [Event(0, 'UE_init') for _ in range(len(ue_list))]
    for event in initial_events:
        scheduler.schedule_event(event)

    scheduler.run_simulation()


if __name__ == "__main__":
    main()
