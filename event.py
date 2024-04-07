class Event:
    def __init__(self, event_time, event_type, event_priority, obj=None, source_node=None, dest_node=None):
        self.event_time = event_time  # Time at which event occurs
        self.event_type = event_type  # Type of the event
        self.source_node = source_node  # Source of the event
        self.dest_node = dest_node  # Destination of the event
        self.obj = obj  # Generic attribute for any object relevant to event
        self.event_priority = event_priority  # Priority of the event

    def __lt__(self, other):
        # Compare event_time and event_priority
        if self.event_time < other.event_time:
            return True
        elif self.event_time > other.event_time:
            return False
        else:
            # If event_time is the same, use event_priority
            return self.event_priority < other.event_priority
