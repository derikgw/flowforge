from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QApplication
from core.plugins.ui_plugin_base import UIPluginBase
from core.events.event_bus import event_bus  # Import the global event bus instance


class ShutdownDialogPlugin(UIPluginBase):
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.function_plugins = []

        # Register for the shutdown event
        event_bus.register("shutdown_app", self.shutdown)

    def on_initialize(self, layout=None, *args, **kwargs):
        """Plugin-specific initialization logic."""
        # Handle additional arguments like main_window if needed
        self.app_logger.info(f"ShutdownDialogPlugin initialized with args: {args}, kwargs: {kwargs}")

    def create_dialog(self, parent=None):
        self.dialog = QDialog(parent)
        self.dialog.setWindowTitle("Shutting Down")
        self.dialog.setModal(True)

        layout = QVBoxLayout()
        self.status_label = QLabel("Preparing to shut down...")
        self.progress_bar = QProgressBar()

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        self.dialog.setLayout(layout)

    def update_status(self, message, progress):
        """Update the status label and progress bar."""
        if self.dialog:
            self.status_label.setText(message)
            self.progress_bar.setValue(progress)

    def show_dialog(self):
        if self.dialog:
            self.dialog.show()

    def close_dialog(self):
        if self.dialog:
            self.dialog.close()

    def shutdown(self):
        self.create_dialog()
        self.show_dialog()

        progress = 0
        for index, plugin in enumerate(self.function_plugins):
            self.update_status(f"Shutting down {plugin.__class__.__name__}...", progress)
            plugin.stop()  # Stop the plugin (this might take time if there are threads)
            progress = int((index + 1) / len(self.function_plugins) * 100)
            QApplication.processEvents()  # Ensure the UI updates

        self.update_status("All plugins stopped. Exiting...", 100)
        QApplication.processEvents()
        self.close_dialog()
