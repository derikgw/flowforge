import os
import logging
from core.plugins.function_plugin_base import FunctionPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class


def load_function_plugins():
    modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
    loaded_plugins = []  # Initialize a list to store loaded plugin instances

    for filename in os.listdir(modules_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Strip off '.py'
            plugin_class = load_plugin_class(module_name)

            if plugin_class and issubclass(plugin_class, FunctionPluginBase):
                instance = plugin_class()
                instance.initialize()  # Assuming initialize is required before starting
                loaded_plugins.append(instance)  # Add the plugin instance to the list
                logging.info(f'Function Plugin {module_name} loaded successfully.')

    return loaded_plugins  # Return the list of loaded plugin instances
