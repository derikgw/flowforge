from PyQt5.QtWidgets import QWidget

from core.plugins.plugin_base import PluginBase


class UIPluginBase(PluginBase):

    def __init__(self):
        super().__init__()

    def initialize(self, layout):
        """Initialize the UI plugin with the provided layout."""
        # Call the initialize method from PluginBase to ensure common logic is executed
        super().initialize(layout=layout)

        # UI-specific initialization logic can go here
        self.on_initialize(layout)

    def get_widget(self):
        """Override this method to return the widget."""
        return None
