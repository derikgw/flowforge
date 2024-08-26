from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget
from core.plugins.ui_plugin_base import UIPluginBase
from core.logging.logger import Logger
from core.events.event_bus import event_bus  # Import the event bus


class PathMonitorUI(UIPluginBase):
    def __init__(self, path_monitor_plugin):
        super().__init__()
        self.path_monitor_plugin = path_monitor_plugin
        self.widget = None

    def on_initialize(self, layout=None, *args, **kwargs):
        """Initialize the UI component for PathMonitorPlugin."""
        self.app_logger.info("Initializing PathMonitorUIPlugin")

        # Create the UI components
        self.widget = QWidget()
        ui_layout = QVBoxLayout()

        # Label
        label = QLabel("Select folder to monitor:")

        # Text box to show selected folder path
        self.folder_path_textbox = QLineEdit(self.path_monitor_plugin.folder_to_monitor)
        self.folder_path_textbox.setReadOnly(True)

        # Button to browse folders
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)

        # Add components to the layout
        ui_layout.addWidget(label)
        ui_layout.addWidget(self.folder_path_textbox)
        ui_layout.addWidget(browse_button)

        self.widget.setLayout(ui_layout)

        # Add the widget to the main layout if provided
        if layout:
            layout.addWidget(self.widget)

        self.app_logger.info("PathMonitorUIPlugin Initialized")

    def browse_folder(self):
        """Open a folder dialog to select the folder to monitor."""
        folder = QFileDialog.getExistingDirectory(None, "Select Folder", self.path_monitor_plugin.folder_to_monitor)

        if folder:
            # Update the text box and the path monitor plugin
            self.folder_path_textbox.setText(folder)

            # Stop the existing monitoring
            self.path_monitor_plugin.stop()

            # Update the folder to monitor
            self.path_monitor_plugin.folder_to_monitor = folder

            # Restart the monitoring with the new folder
            self.path_monitor_plugin.on_initialize()

            self.app_logger.info(f"Monitoring folder updated to: {folder}")

    def get_widget(self):
        """Return the widget for display."""
        return self.widget
