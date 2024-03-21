import argparse
import numpy as np
from event import Event
from ue import UE
from compute_node import ComputeNode
from scheduler import Scheduler


def main(total_simulation_time, num_ue, seed):
    rng = np.random.default_rng(seed=seed)  # Seed for random number generator
    scheduler = Scheduler(total_simulation_time)  # Initializing scheduler for the experiment
    ue_list = [UE(f"UE{i}") for i in range(num_ue)]  # List of UEs
    compute_node = ComputeNode("CN0", scheduler, 0, 0, 0, 20)  # Initializing compute node for the experiment

    scheduler.ue_list = ue_list
    scheduler.compute_node = compute_node

    total_pdus_generated = 0  # Total PDUs generated during the experiment

    for ue in ue_list:
        ue.pdu_session_generation(scheduler)
        pdu_generation_time = rng.integers(1, total_simulation_time)
        pdu_generation_event = Event(pdu_generation_time, 'UE_init', ue)
        scheduler.schedule_event(pdu_generation_event)
        total_pdus_generated += 1

    scheduler.run_simulation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # Run the simulation with user defined arguments
    parser.add_argument("--simulation_time", type=int, default=30)  # Total simulation time for the experiment
    parser.add_argument("--num_ue", type=int, default=4)  # Number of UEs defined for the experiment
    parser.add_argument("--seed", type=int, default=42)  # Seed for random number generator

    # More arguments to be added as required

    args = parser.parse_args()
    main(args.simulation_time, args.num_ue, args.seed)
