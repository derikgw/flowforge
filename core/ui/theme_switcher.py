from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt, QSize


class ThemeSwitcher(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a layout for the switcher
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a label for Dark mode
        self.dark_label = QLabel("Dark")
        layout.addWidget(self.dark_label)

        # Create a checkbox styled as a toggle switch
        self.checkbox = QCheckBox()
        self.checkbox.setTristate(False)
        self.checkbox.setChecked(True)  # Default to Dark mode
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                image: url(':/icons/toggle_on.png');  # Provide custom image or use a better-looking switch
            }
            QCheckBox::indicator:unchecked {
                image: url(':/icons/toggle_off.png');  # Provide custom image or use a better-looking switch
            }
        """)
        layout.addWidget(self.checkbox)

        # Create a label for Light mode
        self.light_label = QLabel("Light")
        layout.addWidget(self.light_label)

        # Connect the checkbox toggle to the theme change function
        self.checkbox.stateChanged.connect(self.toggle_theme)

    def toggle_theme(self, state):
        if state == Qt.Checked:
            self.parent().apply_theme("dark")
        else:
            self.parent().apply_theme("light")
