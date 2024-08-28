import os

from core.logging.logger import Logger


def load_stylesheet(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error loading stylesheet: {e}")
        return ""


def apply_theme(app, theme):
    """Apply the specified theme to the entire application."""
    stylesheet_path = os.path.join(os.getenv('PROJECT_ROOT'), 'styles', f"{theme}_theme.qss")

    try:
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
            app.setStyleSheet(stylesheet)
    except FileNotFoundError:
        print(f"Theme file {stylesheet_path} not found.")