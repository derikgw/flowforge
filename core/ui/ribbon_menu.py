from PyQt5.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt

class RibbonMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Create the Dark/Light theme radio buttons
        self.dark_theme_button = QRadioButton("Dark")
        self.light_theme_button = QRadioButton("Light")
        self.dark_theme_button.setChecked(True)

        # Group the radio buttons
        button_group = QButtonGroup(self)
        button_group.addButton(self.dark_theme_button)
        button_group.addButton(self.light_theme_button)

        # Add the theme options to the right side of the layout
        layout.addStretch(1)
        layout.addWidget(self.dark_theme_button, alignment=Qt.AlignRight)
        layout.addWidget(self.light_theme_button, alignment=Qt.AlignRight)

        # Set fixed height for the ribbon
        self.setFixedHeight(30)  # Adjust as necessary
        self.setStyleSheet("border: 1px solid black; background-color: lightgray;")
