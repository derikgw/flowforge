from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QDockWidget
from core.plugins.plugin_manager import PluginManager
from core.events.event_bus import event_bus
from core.logging.logger import Logger
import os


class MainWindow(QMainWindow):
    def __init__(self, plugin_manager):
        super().__init__()

        self.setWindowTitle("FlowForge")
        self.setGeometry(100, 100, 1280, 720)

        # Initialize logger
        self.app_logger = Logger.get_logger("MainWindowLogger")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Initialize and manage UI plugins, pass self as the main window
        self.plugin_manager = plugin_manager
        self.plugin_manager.initialize_ui_plugins(layout=layout, main_window=self)

        # Load stylesheet
        with open('styles/main.qss', 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # Restore last session layout
        self.restore_last_session()

        # Register for the shutdown event
        event_bus.register("shutdown_app", self.handle_shutdown)

    def closeEvent(self, event):
        """Override the close event to trigger the shutdown process."""
        reply = QMessageBox.question(self, 'Quit',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Save the current layout before closing
            self.save_current_session()

            # Trigger the shutdown process
            self.plugin_manager.trigger_shutdown()
            event.accept()
        else:
            event.ignore()

    def handle_shutdown(self):
        """Handle the shutdown event."""
        self.close()

    def save_current_session(self):
        """Save the current session layout to a file in the .workspace folder."""
        workspace_dir = os.path.join(os.getenv('PROJECT_ROOT'), '.workspace')
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)

        settings_file = os.path.join(workspace_dir, 'window_state.ini')

        with open(settings_file, 'wb') as f:
            f.write(self.saveState())

        self.app_logger.info("Session saved successfully.")

    def restore_last_session(self):
        """Restore the last session layout from the .workspace folder."""
        try:
            workspace_dir = os.path.join(os.getenv('PROJECT_ROOT'), '.workspace')
            settings_file = os.path.join(workspace_dir, 'window_state.ini')

            if os.path.exists(settings_file):
                with open(settings_file, 'rb') as f:
                    self.restoreState(f.read())

                self.app_logger.info("Session restored successfully.")
            else:
                self.app_logger.warning("No previous session found to restore.")
        except Exception as e:
            self.app_logger.error(f"Failed to restore session: {e}")
