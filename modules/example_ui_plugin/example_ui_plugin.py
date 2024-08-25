from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton
from core.plugins.ui_plugin_base import UIPluginBase


class ExampleUiPlugin(UIPluginBase):
    def __init__(self):
        super().__init__()
        self.widget = None

    def on_initialize(self, layout=None, *args, **kwargs):
        """Plugin-specific initialization logic."""

        # Create the button
        self.widget = QPushButton("Click me!")

        # Connect the clicked signal to the click handler
        self.widget.clicked.connect(lambda checked: self.on_click(checked))

        layout.addWidget(self.widget)
        """
        if bool(layout):
            layout.addWidget(self.widget)
            self.app_logger.info("Widget added to layout.")
        else:
            self.app_logger.error("Layout is falsy!")
        """

    @pyqtSlot(bool)
    def on_click(self, checked):
        self.app_logger.info(f"Button was clicked! Checked state is {checked}")

    def get_widget(self):
        return self.widget
