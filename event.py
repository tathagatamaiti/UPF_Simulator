class Event:

    event_counter = 0

    def __init__(self, event_time, event_type, description):
        self.event_id = Event.event_counter
        Event.event_counter += 1
        self.event_time = event_time
        self.event_type = event_type
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        if other.event_id == self.event_id:
            return True
        return False

    def __lt__(self, other):
        if other.event_id == self.event_id:
            return False
        if self.event_time < other.event_time:
            return True
        if self.event_time > other.event_time:
            return False
        return self.event_id < other.event_id

    def get_time(self):
        return self.event_time

    def get_type(self):
        return self.event_type

    def get_description(self):
        return self.description

    def __str__(self):
        return f"{self.event_time:.2f}: {self.description}"
