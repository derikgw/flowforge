import os
from core.plugins.function_plugin_base import FunctionPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class
from core.events.event_bus import event_bus
from core.logging.logger import Logger
from core.plugins.ui_plugin_base import UIPluginBase


class PluginManager:
    def __init__(self):
        self.ui_plugins = []
        self.function_plugins = []
        self.plugin_instances = {}
        self.logger = Logger.get_logger('PluginManager')

    def get_plugin_instance(self, class_name):
        for plugin in self.function_plugins + self.ui_plugins:
            if plugin.__class__.__name__ == class_name:
                return plugin
        return None

    def initialize_ui_plugins(self, layout, main_window):
        self.ui_plugins = self.load_ui_plugins(layout, main_window)

        for plugin in self.ui_plugins:
            plugin.initialize(layout=layout, main_window=main_window)

        # Post an event indicating that all UI plugins have been initialized
        event_bus.post("all_ui_plugins_initialized")

    def initialize_function_plugins(self):
        self.function_plugins = self.load_function_plugins()

        for plugin in self.function_plugins:
            plugin.initialize()

    def load_ui_plugins(self, layout, main_window):
        modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
        loaded_plugins = []

        for module_dir in os.listdir(modules_dir):
            if module_dir == '__pycache__':
                continue

            plugin_class, dependencies = load_plugin_class(module_dir, self)
            if plugin_class and issubclass(plugin_class, UIPluginBase):
                instance = plugin_class(*dependencies)
                self.plugin_instances[plugin_class.__name__] = instance
                loaded_plugins.append(instance)
                self.logger.info(f'UI Plugin {module_dir} loaded successfully.')

        return loaded_plugins

    def load_function_plugins(self):
        modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
        loaded_plugins = []

        for module_dir in os.listdir(modules_dir):
            if module_dir == '__pycache__':
                continue

            plugin_class, dependencies = load_plugin_class(module_dir, self)
            if plugin_class and issubclass(plugin_class, FunctionPluginBase):
                instance = plugin_class(*dependencies)
                self.plugin_instances[plugin_class.__name__] = instance
                loaded_plugins.append(instance)
                self.logger.info(f'Function Plugin {module_dir} loaded successfully.')

        return loaded_plugins if loaded_plugins else []

    def trigger_shutdown(self):
        event_bus.post("shutdown_app")

    def stop_plugins(self):
        for plugin in self.function_plugins:
            plugin.stop()

