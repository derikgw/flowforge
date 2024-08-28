from PyQt5.QtWidgets import QLabel

from core.plugins.ui_plugin_base import UIPluginBase


class DashboardPlugin(UIPluginBase):
    def __init__(self, name, plugin_type, path):
        super().__init__(name, plugin_type, path)

    def initialize(self, main_window=None):
        super().initialize(main_window)
        # Create the widget for this plugin
        self.plugin_widget = QLabel("This is the Dashboard Plugin")
        self.logger.info(f"{self.name} initialized with a QLabel widget.")

    def get_widget(self):
        return self.plugin_widget
