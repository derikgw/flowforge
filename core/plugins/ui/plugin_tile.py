from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class PluginTile(QWidget):
    def __init__(self, plugin_info, is_installed, parent=None):
        super().__init__(parent)

        self.plugin_info = plugin_info
        self.is_installed = is_installed

        layout = QVBoxLayout(self)

        # Plugin Image
        image_label = QLabel(self)
        image_path = plugin_info.get("image", "default_image.png")  # Default image if none is specified
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Plugin Name
        name_label = QLabel(plugin_info["name"], self)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # Install/Uninstall Button
        if is_installed:
            action_button = QPushButton("Uninstall", self)
            action_button.clicked.connect(self.uninstall_plugin)
        else:
            action_button = QPushButton("Install", self)
            action_button.clicked.connect(self.install_plugin)
        layout.addWidget(action_button, alignment=Qt.AlignCenter)

    def install_plugin(self):
        # Logic to install the plugin
        print(f"Installing {self.plugin_info['name']}")
        # Trigger install from PluginManager or Orchestrator

    def uninstall_plugin(self):
        # Logic to uninstall the plugin
        print(f"Uninstalling {self.plugin_info['name']}")
        # Trigger uninstall from PluginManager or Orchestrator
