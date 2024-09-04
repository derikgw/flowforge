import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHeaderView, QHBoxLayout

from core.plugins.plugin_manager import PluginManager


class PluginsView(QWidget):
    def __init__(self, plugin_manager: PluginManager):
        super().__init__()
        self.plugin_manager = plugin_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.plugins_table = QTableWidget()
        self.plugins_table.setColumnCount(4)
        self.plugins_table.setHorizontalHeaderLabels(["Plugin Name", "Installed", "Registered", "Actions"])

        header = self.plugins_table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #2e3b4e;
                color: white;
                padding: 4px;
                font-weight: bold;
                border: 1px solid #2e3b4e;
            }
        """)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        layout.addWidget(self.plugins_table)
        self.setLayout(layout)
        self.refresh_plugins()

    def refresh_plugins(self):
        self.plugins_table.setRowCount(0)

        for plugin_name in os.listdir(self.plugin_manager.plugins_directory):
            plugin_path = os.path.join(self.plugin_manager.plugins_directory, plugin_name)
            if os.path.isdir(plugin_path):
                registered = self.plugin_manager.is_plugin_registered(plugin_name)
                installed = "Yes" if registered else "No"
                registered_text = "Yes" if registered else "No"

                row_position = self.plugins_table.rowCount()
                self.plugins_table.insertRow(row_position)
                self.plugins_table.setItem(row_position, 0, QTableWidgetItem(plugin_name))
                self.plugins_table.setItem(row_position, 1, QTableWidgetItem(installed))
                self.plugins_table.setItem(row_position, 2, QTableWidgetItem(registered_text))

                action_layout = QHBoxLayout()
                if registered:
                    uninstall_button = QPushButton("Uninstall")
                    uninstall_button.clicked.connect(lambda _, n=plugin_name: self.uninstall_plugin(n))
                    action_layout.addWidget(uninstall_button)
                else:
                    install_button = QPushButton("Install")
                    install_button.clicked.connect(lambda _, n=plugin_name, p=plugin_path: self.install_plugin(n, p))
                    action_layout.addWidget(install_button)

                action_widget = QWidget()
                action_widget.setLayout(action_layout)
                self.plugins_table.setCellWidget(row_position, 3, action_widget)

        self.plugins_table.resizeColumnsToContents()

    def install_plugin(self, plugin_name, plugin_path):
        self.plugin_manager.install_plugin(plugin_name, plugin_path)
        self.refresh_plugins()

    def uninstall_plugin(self, plugin_name):
        self.plugin_manager.uninstall_plugin(plugin_name)
        self.refresh_plugins()
