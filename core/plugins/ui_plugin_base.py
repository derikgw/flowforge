from PyQt5.QtWidgets import QWidget
from core.plugins.plugin_base import PluginBase


class UIPluginBase(PluginBase):

    def __init__(self):
        super().__init__()

    def initialize(self, *args, **kwargs):
        """Initialize the UI plugin with the provided layout."""
        super().initialize(*args, **kwargs)  # Ensure that additional kwargs like main_window are passed through

    def get_widget(self):
        """Override this method to return the widget."""
        return None
