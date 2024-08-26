from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QPushButton, QSizePolicy
from core.plugins.ui_plugin_base import UIPluginBase


class ExampleUiPlugin(UIPluginBase):
    def __init__(self):
        super().__init__()
        self.widget = None

    def on_initialize(self, layout=None, main_window=None, *args, **kwargs):
        """Plugin-specific initialization logic."""
        self.app_logger.info("Initializing ExampleUiPlugin")

        # Create the button
        button = QPushButton("Click me!")

        # Connect the clicked signal to the click handler using lambda
        try:
            button.clicked.connect(lambda checked: self.on_click(checked))
            self.app_logger.info("Signal connected successfully with lambda.")
        except Exception as e:
            self.app_logger.error(f"Failed to connect signal: {e}")

        # Create a dock widget
        self.dock_widget = QDockWidget("Example UI Plugin", main_window)
        # Set the object name based on the class name
        self.dock_widget.setObjectName(self.__class__.__name__)

        # Set size policy to make it resizable
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dock_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set minimum size and preferred size
        self.dock_widget.setMinimumSize(200, 100)
        self.dock_widget.resize(300, 150)

        # Set dock widget features
        self.dock_widget.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)

        # Set the widget for the dock
        self.dock_widget.setWidget(button)

        # Add the dock widget to the main window
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)

        self.app_logger.info("ExampleUiPlugin initialized as dockable widget.")

    def on_click(self, checked):
        self.app_logger.info(f"Button was clicked! Checked state is {checked}")

    def get_widget(self):
        return self.dock_widget
