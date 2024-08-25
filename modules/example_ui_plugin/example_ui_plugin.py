from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton
from core.plugins.ui_plugin_base import UIPluginBase


class ExampleUiPlugin(UIPluginBase):
    def __init__(self):
        super().__init__()

        self.app_logger.info("Initializing Example UI Plugin")

        self.widget = QPushButton("Click me!")  # Set the widget to a QPushButton

        # Connect the clicked signal to the click handler
        self.widget.clicked.connect(lambda checked: self.on_click(checked))
        self.app_logger.info("Example UI Plugin Initialized")

    def on_initialize(self, layout=None, *args, **kwargs):
        """Plugin-specific initialization logic."""
        # This method should be flexible enough to handle additional arguments.
        self.app_logger.info(f"Additional args: {args}, kwargs: {kwargs}")

        # Add the widget to the layout if provided
        if layout:
            layout.addWidget(self.widget)

    @pyqtSlot(bool)
    def on_click(self, checked):
        self.app_logger.info(f"Button was clicked! Checked state is {checked}")

    def get_widget(self):
        return self.widget
