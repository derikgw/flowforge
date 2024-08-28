from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QVBoxLayout
import os
import json

from core.plugins.ui.plugin_tile import PluginTile


class PluginPanel(QWidget):
    def __init__(self, plugin_manager, parent=None):
        super().__init__(parent)
        self.plugin_manager = plugin_manager

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Scrollable area to contain the grid of plugins
        scroll_area = QScrollArea(self)
        self.layout.addWidget(scroll_area)

        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)

        self.populate_plugins()

    def populate_plugins(self):
        available_plugins = self.plugin_manager.list_plugins()
        installed_plugins = self.plugin_manager.installed_plugins()

        row, col = 0, 0
        for plugin in available_plugins:
            is_installed = plugin["name"] in installed_plugins
            tile = PluginTile(plugin, is_installed)
            self.grid_layout.addWidget(tile, row, col)
            col += 1
            if col > 3:  # 4 tiles per row
                col = 0
                row += 1
