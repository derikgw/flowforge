import os
import logging
from core.plugins.function_plugin_base import FunctionPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class


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
                instance = plugin_class()  # Initialize without special parameters
                loaded_plugins.append(instance)
                self.logger.info(f'Function Plugin {module_dir} loaded successfully.')

    return loaded_plugins if loaded_plugins else []

