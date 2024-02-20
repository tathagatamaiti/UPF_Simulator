class Event:
    def __init__(self, time, event_type, obj=None):
        self.time = time
        self.event_type = event_type
        self.obj = obj

    def __lt__(self, other):
        return self.time < other.time
