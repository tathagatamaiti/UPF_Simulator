from ue import UE
from compute_node import ComputeNode
from event_manager import EventManager

# Set the threshold for PDU session generation and processing
pdu_limit = 10

# Create instances of ComputeNode, UE, and EventManager
event_manager = EventManager()
compute_node = ComputeNode(event_manager)
ue = UE(compute_node, pdu_limit, event_manager)

# Register UE with the ComputeNode
compute_node.add_upf(ue)

# Generate and process PDUs until the pdu_limit is reached
simulation_clock = 0
while ue.generate_pdu_sessions(simulation_clock, event_manager):
    pass

# Process events
event_manager.process_events()

print("Simulation completed. Output written to output.txt.")
