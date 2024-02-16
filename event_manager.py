class EventManager:
    def __init__(self):
        self.event_queue = []

    def schedule_event(self, event, data=None):
        event.data = data
        self.event_queue.append(event)
        self.event_queue.sort(key=lambda x: x.event_time)

    def process_events(self, total_simulation_time):
        simulation_clock = 0
        while simulation_clock < total_simulation_time and self.event_queue:
            current_event = self.event_queue.pop(0)
            simulation_clock = current_event.event_time
            print(f"Event at time {simulation_clock}: {current_event.description}")
            current_event.handle_event(self)
