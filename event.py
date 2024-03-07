class Event:
    def __init__(self, event_time, event_type, obj=None, source_node=None, dest_node=None, ):
        self.event_time = event_time
        self.event_type = event_type
        self.source_node = source_node
        self.dest_node = dest_node
        self.obj = obj

    def __lt__(self, other):
        return self.event_time < other.event_time
