from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction, QMenuBar, QApplication
from core.logging.logger import Logger
from core.plugins.menu_plugin_base import MenuPluginBase


class MainMenu(MenuPluginBase):

    def __init__(self):
        super().__init__()
        self.menu_bar = None  # Store the menu bar
        self.menu_actions = []  # Store actions to be added to the menu

    def initialize(self, layout):
        self.app_logger.info("Initializing main menu")
        # Create the menu bar
        self.menu_bar = QMenuBar()

        # Add the menu bar to the provided layout
        layout.setMenuBar(self.menu_bar)
        self.add_to_menu_bar(self.menu_bar)

        self.app_logger.info("Main menu initialized")

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

        # Perform any cleanup if necessary

        # Gracefully quit the application
        QApplication.quit()
