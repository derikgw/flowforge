import os
from core.plugins.function_plugin_base import FunctionPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class
from core.events.event_bus import event_bus
from core.logging.logger import Logger
from core.plugins.ui_plugin_base import UIPluginBase


class PluginManager:
    def __init__(self):
        self.ui_plugins = []
        self.function_plugins = []  # Initialize as an empty list
        self.logger = Logger.get_logger('PluginManager')

    def initialize_ui_plugins(self, layout, main_window):
        """Initialize all UI plugins."""
        # Load and initialize UI plugins
        self.ui_plugins = self.load_ui_plugins(layout)

        # Ensure all plugins are initialized
        for plugin in self.ui_plugins:
            plugin.initialize(layout=layout, main_window=main_window)  # Pass the main window reference

    def initialize_function_plugins(self):
        """Initialize all function plugins."""
        # Load and initialize function plugins
        self.function_plugins = self.load_function_plugins()

        # Ensure all plugins are initialized
        if self.function_plugins is None:
            self.function_plugins = []  # Fallback to an empty list if None

        for plugin in self.function_plugins:
            plugin.initialize()

    def load_ui_plugins(self, layout):
        """Load and initialize UI plugins."""
        modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
        loaded_plugins = []
        for module_dir in os.listdir(modules_dir):
            if module_dir == '__pycache__':
                continue  # Skip __pycache__ directories

            module_path = os.path.join(modules_dir, module_dir)
            if os.path.isdir(module_path):
                plugin_class = load_plugin_class(module_dir)
                if plugin_class and issubclass(plugin_class, UIPluginBase):
                    instance = plugin_class()
                    loaded_plugins.append(instance)
                    self.logger.info(f'UI Plugin {module_dir} loaded successfully.')
        return loaded_plugins

    def load_function_plugins(self):
        """Load and initialize function plugins."""
        modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
        loaded_plugins = []
        for module_dir in os.listdir(modules_dir):
            if module_dir == '__pycache__':
                continue  # Skip __pycache__ directories

            module_path = os.path.join(modules_dir, module_dir)
            if os.path.isdir(module_path):
                plugin_class = load_plugin_class(module_dir)
                if plugin_class and issubclass(plugin_class, FunctionPluginBase):
                    instance = plugin_class()
                    loaded_plugins.append(instance)
                    self.logger.info(f'Function Plugin {module_dir} loaded successfully.')

        return loaded_plugins if loaded_plugins else []

    def trigger_shutdown(self):
        """Trigger the shutdown process via the event bus."""
        event_bus.post("shutdown_app")

    def stop_plugins(self):
        """Stop all function plugins."""
        for plugin in self.function_plugins:
            plugin.stop()

