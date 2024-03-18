import numpy as np
from event import Event
from ue import UE
from compute_node import ComputeNode
from scheduler import Scheduler

# DEFINING EXPERIMENT PARAMETERS

total_simulation_time = "TOTAL SIMULATION TIME FOR THE EXPERIMENT"
num_ue = "NUMBER OF UEs DEFINED FOR THE EXPERIMENT"
seed = "SEED DEFINED FOR REPRODUCING RESULTS"
total_pdus_generated = "TOTAL PDUs GENERATED DURING THE EXPERIMENT"


def main():
    rng = np.random.default_rng(seed=42)  # Using NumPy's random number generator for seeding
    total_simulation_time = 30
    num_ue = 4
    scheduler = Scheduler(total_simulation_time)
    ue_list = [UE(f"UE{i}") for i in range(num_ue)]
    compute_node = ComputeNode("CN0", scheduler, 0, 0, 0, 20)
    total_pdus_generated = 0

    scheduler.ue_list = ue_list
    scheduler.compute_node = compute_node

    for ue in ue_list:
        ue.pdu_session_generation(scheduler)
        pdu_generation_time = rng.integers(1, total_simulation_time)  # Using NumPy's random integer generator
        pdu_generation_event = Event(pdu_generation_time, 'UE_init', ue)
        scheduler.schedule_event(pdu_generation_event)
        total_pdus_generated += 1

    scheduler.run_simulation()


if __name__ == "__main__":
    main()
