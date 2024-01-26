import heapq

class EventManager:
    def __init__(self, output_file='output.txt'):
        self.event_queue = []
        self.simulation_clock = 0
        self.output_file = output_file

    def schedule_event(self, delay, description):
        event_time = self.simulation_clock + delay
        # Check if an event with the same description already exists
        if not any(desc == description for _, desc in self.event_queue):
            heapq.heappush(self.event_queue, (event_time, description))

    def process_events(self):
        with open(self.output_file, 'w') as file:
            while self.event_queue:
                event_time, description = heapq.heappop(self.event_queue)
                self.simulation_clock = event_time
                file.write(f"{description}\n")
