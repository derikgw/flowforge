from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton
from core.plugins.ui_plugin_base import UIPluginBase


class ExampleUiPlugin(UIPluginBase):
    def __init__(self):
        super().__init__()
        self.widget = QPushButton("Click me!")  # Create the widget

    def on_initialize(self, layout=None):
        """Plugin-specific initialization logic."""
        # Connect the clicked signal to the click handler
        self.widget.clicked.connect(lambda checked: self.on_click(checked))
        self.app_logger.info("Example UI Plugin Initialized")

    @pyqtSlot(bool)
    def on_click(self, checked):
        self.app_logger.info(f"Button was clicked! Checked state is {checked}")

    def get_widget(self):
        return self.widget
