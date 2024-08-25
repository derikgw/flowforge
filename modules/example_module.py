from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton
from core.plugin_base import PluginBase

class ExampleModule(PluginBase):
    def __init__(self):
        super().__init__()
        self.widget = QPushButton("Click me!")  # Set the widget to a QPushButton

        # Connect the clicked signal to the click handler
        self.widget.clicked.connect(lambda checked: self.on_click(checked))

    @pyqtSlot(bool)
    def on_click(self, checked):
        print(f"Button was clicked! Checked state is {checked}")

    def get_widget(self):
        return self.widget
