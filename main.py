import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from core.logging.logger import Logger
from core.ui.styles import apply_theme
from core.web.proxy import start_proxy_service
from core.ui.main_window import MainWindow
from core.plugins.plugin_manager import PluginManager

# Dynamically determine the project root directory
project_root_path = Path(__file__).resolve().parent
os.environ['PROJECT_ROOT'] = str(project_root_path)

# Load the logger configuration
Logger.load_config()


def initialize_application(app):
    # Initialize the application and retrieve loggers by name
    app_logger = Logger.get_logger("app_logger")
    app_logger.info("Application starting...")

    # Determine the proxy port from environment or use default
    proxy_port = int(os.getenv('FLOWFORGE_PROXY_PORT', 8000))
    start_proxy_service(port=proxy_port)

    # Initialize plugins using the PluginManager
    plugins_directory = os.path.join(os.getenv('PROJECT_ROOT'), 'plugins')
    plugin_manager = PluginManager(plugins_directory)

    # Apply a default theme
    apply_theme(app, "dark")  # or "light" based on preference
    app.processEvents()  # Forces the application to process all pending events

    return plugin_manager


def main():
    # Create the main window and start the UI
    app = QApplication([])

    plugin_manager = initialize_application(app)

    window = MainWindow(plugin_manager)
    window.show()
    app.exec_()

    plugin_manager.stop_all_plugins()


if __name__ == "__main__":
    main()
