import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from core.logging.logger import Logger
from ui.main_window import MainWindow
from core.plugins.plugin_manager import PluginManager

# Dynamically determine the project root directory
project_root_path = Path(__file__).resolve().parent
os.environ['PROJECT_ROOT'] = str(project_root_path)

# Load the logger configuration
Logger.load_config()


def initialize_application():
    # Initialize the application and retrieve loggers by name
    app_logger = Logger.get_logger("app_logger")
    error_logger = Logger.get_logger("error_logger")
    app_logger.info("Application starting...")
    # Initialize function plugins
    plugin_manager = PluginManager()
    plugin_manager.initialize_function_plugins()  # Only load function plugins

    return plugin_manager


def main():
    plugin_manager = initialize_application()

    # Create the main window and start the UI
    app = QApplication([])
    window = MainWindow(plugin_manager)  # UI plugins will be initialized within MainWindow
    window.show()
    app.exec_()

    # Stop all function plugins before exiting the application
    plugin_manager.stop_plugins()


if __name__ == "__main__":
    main()
