from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHeaderView, QMessageBox
)
from core.plugins.plugin_manager import PluginManager
from core.plugins.plugin_installer import PluginInstaller  # Import the installer


class PluginsView(QWidget):
    def __init__(self, plugin_manager: PluginManager):
        super().__init__()
        self.plugin_manager = plugin_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the Plugins View UI."""
        layout = QVBoxLayout()

        # Create the table to display plugins
        self.plugins_table = QTableWidget()
        self.plugins_table.setColumnCount(4)
        self.plugins_table.setHorizontalHeaderLabels(["Plugin Name", "Installed", "Registered", "Actions"])

        # Set header style for better visibility and aesthetics
        header = self.plugins_table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #2e3b4e;  /* Darker background */
                color: white;               /* White text */
                padding: 4px;               /* Add some padding */
                font-weight: bold;          /* Bold text */
                border: 1px solid #2e3b4e;  /* Border to match background */
            }
        """)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        layout.addWidget(self.plugins_table)

        # Create a refresh button
        refresh_button = QPushButton("Refresh Plugins")
        refresh_button.clicked.connect(self.refresh_plugins)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.refresh_plugins()

    def refresh_plugins(self):
        """Refresh the plugin list in the view."""
        self.plugins_table.setRowCount(0)  # Clear the table

        # Get available plugins from the database (assuming PluginManager has access to the database)
        plugins_info = self.plugin_manager.get_all_plugins()  # This method needs to be added to PluginManager

        for plugin in plugins_info:
            plugin_name = plugin["name"]
            installed = "Yes" if plugin["installed"] else "No"
            registered = "Yes" if plugin["registered"] else "No"

            row_position = self.plugins_table.rowCount()
            self.plugins_table.insertRow(row_position)

            self.plugins_table.setItem(row_position, 0, QTableWidgetItem(plugin_name))
            self.plugins_table.setItem(row_position, 1, QTableWidgetItem(installed))
            self.plugins_table.setItem(row_position, 2, QTableWidgetItem(registered))

            # Add an install/uninstall button based on the installation status
            if not plugin["installed"]:
                install_button = QPushButton("Install")
                install_button.clicked.connect(lambda _, p=plugin_name: self.install_plugin(p))
                self.plugins_table.setCellWidget(row_position, 3, install_button)
            else:
                uninstall_button = QPushButton("Uninstall")
                uninstall_button.clicked.connect(lambda _, p=plugin_name: self.uninstall_plugin(p))
                self.plugins_table.setCellWidget(row_position, 3, uninstall_button)

        self.plugins_table.resizeColumnsToContents()  # Adjust columns to fit content

    def install_plugin(self, plugin_name):
        """Install a selected plugin."""
        plugin_directory = self.plugin_manager.get_plugin_directory(plugin_name)
        try:
            PluginInstaller.install(plugin_name, plugin_directory)
            QMessageBox.information(self, "Success", f"Plugin '{plugin_name}' installed successfully.")
            self.refresh_plugins()  # Refresh the plugin list after installation
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to install plugin '{plugin_name}': {e}")

    def uninstall_plugin(self, plugin_name):
        """Uninstall a selected plugin."""
        try:
            self.plugin_manager.uninstall_plugin(plugin_name)
            QMessageBox.information(self, "Success", f"Plugin '{plugin_name}' uninstalled successfully.")
            self.refresh_plugins()  # Refresh the plugin list after uninstallation
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to uninstall plugin '{plugin_name}': {e}")
