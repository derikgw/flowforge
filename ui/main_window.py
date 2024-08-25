from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from core.plugins.plugin_manager import PluginManager  # Import the PluginManager
from core.events.event_bus import event_bus


class MainWindow(QMainWindow):
    def __init__(self, plugin_manager):
        super().__init__()

        self.setWindowTitle("FlowForge")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Initialize and manage UI plugins, pass self as the main window
        self.plugin_manager = plugin_manager
        self.plugin_manager.initialize_ui_plugins(layout=layout, main_window=self)  # Pass the main window

        # Load stylesheet
        with open('styles/main.qss', 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # Register for the shutdown event
        event_bus.register("shutdown_app", self.handle_shutdown)

    def closeEvent(self, event):
        """Override the close event to trigger the shutdown process."""
        reply = QMessageBox.question(self, 'Quit',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Trigger the shutdown process
            self.plugin_manager.trigger_shutdown()
            event.accept()
        else:
            event.ignore()

    def handle_shutdown(self):
        """Handle the shutdown event."""
        self.close()


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
        self.app_logger.info("Initializing MainMenu")

        # Create the menu bar
        self.menu_bar = QMenuBar()

        # Check if the main window is provided and add the menu bar
        if main_window:
            main_window.setMenuBar(self.menu_bar)
            self.app_logger.info("Menu bar set to main window")

        # Add items to the menu bar
        self.add_to_menu_bar(self.menu_bar)

        self.app_logger.info("MainMenu initialized")

    def add_to_menu_bar(self, menu_bar):
        # Create a File menu
        file_menu = menu_bar.addMenu("File")

        # Add the default Exit action
        exit_action = QAction("Exit", menu_bar)
        exit_action.triggered.connect(self.on_exit)
        file_menu.addAction(exit_action)

        # Add dynamically configured actions
        for action in self.menu_actions:
            file_menu.addAction(action)

    def add_menu_action(self, action):
        """Add a QAction to the menu. Plugins can call this method to add their actions."""
        self.menu_actions.append(action)

    @pyqtSlot()
    def on_exit(self):
        self.app_logger.info("Exiting the application...")

        # Post the shutdown event to the event bus
        event_bus.post("shutdown_app")

        # Perform any additional cleanup if necessary
        self.app_logger.info("Shutdown event posted.")
