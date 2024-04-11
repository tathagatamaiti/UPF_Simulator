import argparse
import numpy as np
import sys
from event import Event
from events import Events
from ue import UE
from compute_node import ComputeNode
from scheduler import Scheduler


def main(total_simulation_time, num_ue, seed, output_file):
    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Redirect stdout to the file
        sys.stdout = f

        rng = np.random.default_rng(seed=seed)  # Seed for random number generator
        scheduler = Scheduler(total_simulation_time)  # Initializing scheduler for the experiment
        ue_list = [UE(f"UE{i}") for i in range(num_ue)]  # List of UEs
        compute_node = ComputeNode("CN0", scheduler, 0, 0, 0, 3)  # Initializing compute node for the experiment

        scheduler.ue_list = ue_list
        scheduler.compute_node = compute_node

        total_pdus_generated = 0  # Total PDUs generated during the experiment

        for ue in ue_list:
            ue.pdu_session_generation(scheduler)
            pdu_generation_time = rng.integers(1, total_simulation_time)
            pdu_generation_event = Event(pdu_generation_time, Events.UE_init, 0, ue)
            scheduler.schedule_event(pdu_generation_event)
            total_pdus_generated += 1

        scheduler.run_simulation()

    # Reset stdout to its default value after writing to the file
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # Run the simulation with user defined arguments
    parser.add_argument("--simulation_time", type=int, default=40)  # Total simulation time for the experiment
    parser.add_argument("--num_ue", type=int, default=4)  # Number of UEs defined for the experiment
    parser.add_argument("--seed", type=int, default=42)  # Seed for random number generator
    parser.add_argument("--sim_num_pdu", type=int, default=20)  # Total number of PDUs in the simulation
    parser.add_argument("--upf_c", type=int, default=3)  # Capacity of a UPF in terms of number of PDUs it can handle
    # parser.add_argument("--mu", type=int, default=)  # average duration of PDUs
    # parser.add_argument("--lambda", type=int, default=)  # inter-arrival time between PDU at each UE
    parser.add_argument("--output_file", type=str, default="output.txt")  # Output file for storing the results

    args = parser.parse_args()
    main(args.simulation_time, args.num_ue, args.seed, args.output_file)
