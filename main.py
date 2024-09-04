import os
from pathlib import Path
import yaml
from PyQt5.QtWidgets import QApplication
from core.logging.logger import Logger
from core.ui.styles import apply_theme
from core.web.proxy import start_proxy_service
from core.ui.main_window import MainWindow
from core.plugins.plugin_manager import PluginManager
from core.plugins.plugin_installer import PluginInstaller

# Dynamically determine the project root directory
project_root_path = Path(__file__).resolve().parent
os.environ['PROJECT_ROOT'] = str(project_root_path)


def load_configs():
    # Load the logger configuration
    logger_config = os.path.join(os.environ['PROJECT_ROOT'], 'config', 'logger_config.yaml')
    Logger.load_config(logger_config)

    # Load the database configuration
    db_config_path = os.path.join(os.environ['PROJECT_ROOT'], 'config', 'db_config.yaml')
    with open(db_config_path, 'r') as db_config_file:
        return yaml.safe_load(db_config_file)


def create_database_if_not_exists(db_path):
    """Create the database and the necessary table if it doesn't exist."""
    plugin_installer = PluginInstaller(db_path)

    # Example table creation (you can adjust this to your needs)
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS plugins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        version VARCHAR(255),
        description TEXT,
        entry_point VARCHAR(255),
        type VARCHAR(50),
        path TEXT,
        communication_protocol VARCHAR(50)
    );
    """
    plugin_installer._execute_query(table_creation_query)
    plugin_installer.close()


def initialize_application(app):
    # Load the configuration from YAML
    config = load_configs()

    # Initialize the application and retrieve loggers by name
    app_logger = Logger.get_logger("app_logger")
    error_logger = Logger.get_logger("error_logger")
    app_logger.info("Application starting...")

    # Determine the proxy port from environment or use default
    proxy_port = int(os.getenv('FLOWFORGE_PROXY_PORT', 8000))
    start_proxy_service(port=proxy_port)

    # Initialize PluginManager with database path from config
    db_path = config['database']['path']

    # Ensure the database and necessary tables are created
    create_database_if_not_exists(db_path)

    plugin_manager = PluginManager(plugins_directory='plugins', db_path=db_path)

    # Apply a default theme
    apply_theme(app, "dark")  # or "light" based on preference
    app.processEvents()

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
