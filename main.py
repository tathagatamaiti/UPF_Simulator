import argparse
from scheduler import Scheduler
from compute_node import ComputeNode
from ue import UE
from event import Event
import random


def main():
    parser = argparse.ArgumentParser(description='Simulate UPF processing of PDUs')
    parser.add_argument('n', type=int, help='Number of UEs')
    parser.add_argument('seed', type=int, help='Seed to be used for random number generator')
    parser.add_argument('upfc', type=int, help='Capacity of an UPF in terms of number of PDUs it can handle')
    parser.add_argument('sim_duration', type=int, help='Total simulation duration')
    parser.add_argument('sim_num_pdu', type=int, help='Number of PDUs to simulate')

    args = parser.parse_args()

    random.seed(args.seed)

    # Create Compute Node
    ComputeNode(args.upfc, 0, 0, 0, 0, args.sim_num_pdu)

    # Create UEs
    ue_list = [UE(f"UE{i}") for i in range(args.n)]

    # Create Scheduler
    scheduler = Scheduler(args.sim_duration)

    # Generate initial UE events
    for ue in ue_list:
        init_event = Event(0, 'UE_init', ue)
        scheduler.schedule_event(init_event)

    # Generate additional PDU request events
    for i in range(args.sim_num_pdu):
        ue = random.choice(ue_list)
        pdu_session = ue.generate_pdu_session()
        pdu_request_event = Event(random.expovariate(1 / args.lambda_val), 'PDU_request', pdu_session)
        scheduler.schedule_event(pdu_request_event)

    # Run simulation
    scheduler.run_simulation()


if __name__ == "__main__":
    main()

