import heapq
import sys


class EventManager:
    def __init__(self, output_file='output.txt'):
        self.event_queue = []
        self.simulation_clock = 0
        self.output_file = output_file

    def schedule_event(self, event):
        event.get_time()
        if not any(e.get_type() == event.get_type() and e.get_description() == event.get_description() for e in
                   self.event_queue):
            heapq.heappush(self.event_queue, event)

    def process_events(self):
        with open(self.output_file, 'w') as file:
            while self.event_queue:
                event = heapq.heappop(self.event_queue)
                self.simulation_clock = event.get_time()
                file.write(f"{event}\n")

    def get_simulation_clock(self):
        return self.simulation_clock

    def next_event(self):
        try:
            event = heapq.heappop(self.event_queue)
            self.simulation_clock = event.get_time()
            return event
        except IndexError:
            print("No more events in the simulation queue. Terminating.")
            sys.exit(0)
