# ui/main_window.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from core.module_loader import load_modules  # Updated import


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Workflow Portal")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowIcon(QIcon('assets/icon.png'))

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Dynamically load all modules
        load_modules(layout)

        # Load stylesheet
        with open('styles/main.qss', 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())
