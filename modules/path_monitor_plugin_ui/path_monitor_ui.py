from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget
from core.plugins.ui_plugin_base import UIPluginBase
from core.events.event_bus import event_bus  # Import the event bus


class PathMonitorUI(UIPluginBase):
    def __init__(self, path_monitor_plugin):
        super().__init__()
        self.path_monitor_plugin = path_monitor_plugin
        self.dock_widget = None  # Store the dock widget

    def on_initialize(self, layout=None, main_window=None, *args, **kwargs):
        """Initialize the UI component for PathMonitorPlugin."""
        self.app_logger.info("Initializing PathMonitorUIPlugin")

        # Create the dock widget
        self.dock_widget = QDockWidget("Path Monitor UI Plugin", main_window)

        # Create the main widget and set it as the dock widget's widget
        self.widget = self.create_widget()
        self.dock_widget.setWidget(self.widget)
        # Set the object name based on the class name
        self.dock_widget.setObjectName(self.__class__.__name__)

        # Set the dock widget's size policy
        self.dock_widget.setSizePolicy(QWidget.sizePolicy(self.widget))

        # Set minimum size and preferred size
        self.dock_widget.setMinimumSize(300, 150)
        self.dock_widget.resize(400, 200)

        # Set dock widget features
        self.dock_widget.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)

        # Add the dock widget to the main window
        main_window.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        self.app_logger.info("PathMonitorUIPlugin initialized as dockable widget.")

    def create_widget(self):
        """Create and return the main widget for this plugin."""
        self.app_logger.info("Creating widget for PathMonitorUIPlugin")

        # Create the UI components
        widget = QWidget()
        ui_layout = QVBoxLayout()

        # Add some padding to the layout
        ui_layout.setContentsMargins(10, 10, 10, 10)
        ui_layout.setSpacing(10)

        # Label
        label = QLabel("Select folder to monitor:")
        label.setStyleSheet("font-weight: bold;")

        # Text box to show selected folder path
        self.folder_path_textbox = QLineEdit(self.path_monitor_plugin.folder_to_monitor)
        self.folder_path_textbox.setReadOnly(True)
        self.folder_path_textbox.setStyleSheet("padding: 5px;")

        # Button to browse folders
        browse_button = QPushButton("Browse")
        browse_button.setStyleSheet("padding: 5px;")
        browse_button.clicked.connect(self.browse_folder)

        # Add components to the layout
        ui_layout.addWidget(label)
        ui_layout.addWidget(self.folder_path_textbox)
        ui_layout.addWidget(browse_button, alignment=Qt.AlignRight)

        widget.setLayout(ui_layout)
        return widget

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
        return self.dock_widget
