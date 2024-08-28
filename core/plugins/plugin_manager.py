import os
from core.events.event_bus import event_bus
from core.logging.logger import Logger
from core.plugins.plugin_base import Plugin

class PluginManager:
    def __init__(self, plugins_directory):
        self.plugins = []
        self.plugin_instances = {}
        self.logger = Logger.get_logger('PluginManager')
        self.plugins_directory = plugins_directory

    def initialize_plugins(self, main_window):
        self.plugins = self.load_plugins()

        for plugin in self.plugins:
            plugin_type = plugin.get_type()
            if plugin_type == "UI":
                plugin.initialize(main_window=main_window)
            elif plugin_type == "Function":
                plugin.initialize()

        event_bus.post("all_plugins_initialized")

    def load_plugins(self):
        plugins = []
        for plugin_name in os.listdir(self.plugins_directory):
            plugin_path = os.path.join(self.plugins_directory, plugin_name)
            if os.path.isdir(plugin_path):
                plugin_instance = self._load_plugin(plugin_name, plugin_path)
                if plugin_instance:
                    plugins.append(plugin_instance)
        return plugins

    def _load_plugin(self, plugin_name, plugin_path):
        try:
            plugin_type = "UI" if "ui" in plugin_name.lower() else "Function"
            # Assuming Plugin is the base class; actual plugins should subclass Plugin
            return Plugin(plugin_name, plugin_type, plugin_path)
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return None

    def get_plugins_by_type(self, plugin_type):
        """Return a list of plugins filtered by type."""
        return [plugin for plugin in self.plugins if plugin.get_type() == plugin_type]

    def get_all_plugins(self):
        """Return all loaded plugins."""
        return self.plugins

    def stop_all_plugins(self):
        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'stop'):
                    plugin.stop()
            except Exception as e:
                self.logger.error(f"Failed to stop plugin {plugin.get_name()}: {e}")
        self.logger.info("All plugins have been stopped.")
