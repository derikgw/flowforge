from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction, QMenuBar, QApplication

from core.events.event_bus import event_bus
from core.plugins.ui_plugin_base import UIPluginBase


class MainMenu(UIPluginBase):
    def __init__(self):
        super().__init__()
        self.menu_bar = None  # Store the menu bar
        self.menu_actions = []  # Store actions to be added to the menu

    def on_initialize(self, layout=None, main_window=None):
        """Plugin-specific initialization logic."""
        # Create the menu bar
        self.menu_bar = QMenuBar()

        # Check if the main window is provided and add the menu bar
        if main_window:
            main_window.setMenuBar(self.menu_bar)
            self.app_logger.info("Menu bar set to main window")

        # Add items to the menu bar
        self.add_to_menu_bar(self.menu_bar)

    def add_to_menu_bar(self, menu_bar):
        # Create a File menu
        file_menu = menu_bar.addMenu("File")

        # Add the default Exit action
        exit_action = QAction("Exit", menu_bar)
        exit_action.triggered.connect(lambda: self.on_exit(False))
        file_menu.addAction(exit_action)

        # Add dynamically configured actions
        for action in self.menu_actions:
            file_menu.addAction(action)

    def add_menu_action(self, action):
        """Add a QAction to the menu. Plugins can call this method to add their actions."""
        self.menu_actions.append(action)

    @pyqtSlot(bool)
    def on_exit(self, checked):
        self.app_logger.info("Exiting the application...")

        # Post the shutdown event to the event bus
        event_bus.post("shutdown_app")

        # Perform any additional cleanup if necessary

        self.app_logger.info("Shutdown event posted.")


