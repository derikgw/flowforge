import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from core.logging.logger import Logger
from ui.main_window import MainWindow
from core.plugins.function_plugin_loader import load_function_plugins

# Dynamically determine the project root directory
# Assume the project root is the directory containing this script
project_root_path = Path(__file__).resolve().parent

# Set PROJECT_ROOT environment variable
os.environ['PROJECT_ROOT'] = str(project_root_path)


def initialize_function_plugins():
    # Load and start function plugins
    function_plugins = load_function_plugins()

    # Start all loaded plugins
    for plugin in function_plugins:
        plugin.start()

    # Store the plugin instances if you need to manage them later
    return function_plugins


def initialize_application():
    # Retrieve loggers by name
    app_logger = Logger.get_logger("app_logger")
    error_logger = Logger.get_logger("error_logger")


def main():
    # Initialize the application
    initialize_application()

    # Start function plugins
    function_plugins = initialize_function_plugins()

    # Create the main window and start the UI
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

    # Example: Stop plugins before exiting the application
    for plugin in function_plugins:
        plugin.stop()


if __name__ == "__main__":
    main()
