class EventBus:
    def __init__(self):
        self.listeners = {}

    def register(self, event_name, listener):
        """Register a listener for a specific event."""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def unregister(self, event_name, listener):
        """Unregister a listener for a specific event."""
        if event_name in self.listeners:
            self.listeners[event_name].remove(listener)

    def post(self, event_name, *args, **kwargs):
        """Post an event to all registered listeners."""
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(*args, **kwargs)

# Create a global event bus instance
event_bus = EventBus()
