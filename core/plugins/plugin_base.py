from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, name, plugin_type, path):
        self.name = name
        self.plugin_type = plugin_type
        self.path = path

    def get_name(self):
        return self.name

    def get_type(self):
        return self.plugin_type

    def get_path(self):
        return self.path

    @abstractmethod
    def initialize(self):
        """Initialize the plugin."""
        pass

    def stop(self):
        """Stop the plugin (optional)."""
        pass

    def get_widget(self):
        """Return the UI widget if applicable (for UI plugins)."""
        return None
