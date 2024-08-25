from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from core.plugins.ui_plugin_loader import load_ui_plugins


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FlowForge")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Dynamically load all plugins
        load_ui_plugins(layout=layout)  # Pass the layout to the plugins

        # Load stylesheet
        with open('styles/main.qss', 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())
