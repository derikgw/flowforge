from PyQt5.QtWidgets import QWidget

from core.plugins.plugin_base import PluginBase


class UIPluginBase(PluginBase):

    def __init__(self):
        super().__init__()

    def initialize(self, layout):
        """Initialize the UI plugin with the provided layout."""
        pass

    def get_widget(self):
        """Override this method to return the widget."""
        return None
