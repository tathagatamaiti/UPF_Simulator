import argparse
import csv
import numpy as np
import sys

from compute_node import ComputeNode
from event import Event
from events import Events
from scheduler import Scheduler
from ue import UE


def main(total_simulation_time, num_ue, seed, sim_num_pdu, max_upfs, t, output_file, T1, T2):
    # Open the output file in write mode
    with open(output_file, 'w') as f, open('output.csv', 'w', newline='') as csv_file:
        # Redirect stdout to the file
        sys.stdout = f
        writer = csv.writer(csv_file)
        writer.writerow(['sim_time', 'PDU', 'UPF'])

        rng = np.random.default_rng(seed=seed)  # Seed for random number generator
        scheduler = Scheduler(total_simulation_time, max_upfs, t, writer)  # Initializing scheduler for the experiment
        ue_list = [UE(f"UE{i}") for i in range(num_ue)]  # List of UEs
        compute_node = ComputeNode("CN0", scheduler, 0, 0, 0, max_upfs, t, writer, T1,
                                   T2, 1)  # Initializing compute node for the experiment

        scheduler.ue_list = ue_list
        scheduler.compute_node = compute_node

        total_pdus_generated = 0  # Total PDUs generated during the experiment

        for ue in ue_list:
            ue.pdu_session_generation(scheduler, writer)
            pdu_generation_time = rng.integers(1, total_simulation_time)
            pdu_generation_event = Event(pdu_generation_time, Events.UE_init, 0, ue)
            scheduler.schedule_event(pdu_generation_event)
            total_pdus_generated += 1

        scheduler.run_simulation()

    # Reset stdout to its default value after writing to the file
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # Run the simulation with user defined arguments
    parser.add_argument("--simulation_time", type=int, default=50)  # Total simulation time for the experiment
    parser.add_argument("--num_ue", type=int, default=4)  # Number of UEs defined for the experiment
    parser.add_argument("--seed", type=int, default=42)  # Seed for random number generator
    parser.add_argument("--sim_num_pdu", type=int, default=20)  # Total number of PDUs in the simulation
    parser.add_argument("--max_upfs", type=int, default=2)  # Maximum number of UPFs allowed during simulation
    parser.add_argument("--t", type=int, default=2)  # Maximum slots in a UPF
    parser.add_argument("--output_file", type=str, default="output.txt")  # Output file for storing the results
    parser.add_argument("--T1", type=int, default=5)  # Threshold T1
    parser.add_argument("--T2", type=int, default=2)  # Threshold T2

    args = parser.parse_args()
    main(args.simulation_time, args.num_ue, args.seed, args.sim_num_pdu, args.max_upfs, args.t, args.output_file,
         args.T1, args.T2)
