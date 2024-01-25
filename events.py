class EventManager:
    def __init__(self):
        self.events = []

    def schedule_event(self, simulation_clock, event_message):
        self.events.append((simulation_clock, event_message))

    def print_events(self):
        for event in sorted(self.events, key=lambda x: x[0]):
            print(f"{event[0]:.2f}: {event[1]}")

    def write_events_to_file(self, filename):
        with open(filename, "w") as file:
            for event in sorted(self.events, key=lambda x: x[0]):
                file.write(f"{event[0]:.2f}: {event[1]}\n")
