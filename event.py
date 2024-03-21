class Event:
    def __init__(self, event_time, event_type, obj=None, source_node=None, dest_node=None, ):
        self.event_time = event_time  # Time at which event occurs
        self.event_type = event_type  # Type of the event
        self.source_node = source_node  # Source of the event
        self.dest_node = dest_node  # Destination of the event
        self.obj = obj

    def __lt__(self, other):
        return self.event_time < other.event_time
