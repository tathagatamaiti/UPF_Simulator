import random

from event import Event
from ue import UE
from compute_node import ComputeNode
from scheduler import Scheduler


def main():
    random.seed(42)
    total_simulation_time = 30
    num_ue = 3
    scheduler = Scheduler(total_simulation_time)
    ue_list = [UE(f"UE{i}") for i in range(num_ue)]
    compute_node = ComputeNode("CN0", scheduler, 0, 0, 0)
    total_pdus_generated = 0

    scheduler.ue_list = ue_list
    scheduler.compute_node = compute_node

    for ue in ue_list:

        ue.generate_pdu_session()
        pdu_generation_time = random.randint(1, total_simulation_time)
        pdu_generation_event = Event(pdu_generation_time, 'UE_init', ue)
        scheduler.schedule_event(pdu_generation_event)
        total_pdus_generated += 1

    scheduler.run_simulation()


if __name__ == "__main__":
    main()
