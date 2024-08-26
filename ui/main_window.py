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
        self.plugin_manager.initialize_ui_plugins(layout=layout, main_window=self)  # Pass the main window and layout

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
