import sys
import heapq
from event import Event


class EventManager:
    def __init__(self, output_file='output.txt'):
        self.event_queue = []
        self.simulation_clock = 0
        self.output_file = output_file
        self.event_objects = {}

    def create_event(self, event_time, event_type, description, obj=None):
        event = Event(event_time, event_type, description)
        if obj:
            self.event_objects[description] = obj
        return event

    def schedule_event(self, event):
        event_time = event.get_time()
        self.simulation_clock = event_time
        if not any(e.get_type() == event.get_type() and e.get_description() == event.get_description() for e in
                   self.event_queue):
            heapq.heappush(self.event_queue, event)

    def next_event(self):
        try:
            event = heapq.heappop(self.event_queue)
            self.simulation_clock = event.get_time()
            return event
        except IndexError:
            print("No more events in the simulation queue. Terminating.")
            sys.exit(0)

    def process_events(self):
        with open(self.output_file, 'w') as file:
            while self.event_queue:
                event = heapq.heappop(self.event_queue)
                self.simulation_clock = event.get_time()
                file.write(f"{event}\n")

    def get_simulation_clock(self):
        return self.simulation_clock

    def has_events(self):
        return bool(self.event_queue)

    def get_object(self, description):
        return self.event_objects.get(description)

    def get_objects(self, obj_type):
        return [obj for obj in self.event_objects.values() if obj_type in obj_type.lower()]
