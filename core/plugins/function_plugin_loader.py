import os
import logging
from core.plugins.function_plugin_base import FunctionPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class


def load_function_plugins():
    modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
    loaded_plugins = []

    for module_dir in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_dir)
        if os.path.isdir(module_path):
            module_init_file = os.path.join(module_path, '__init__.py')
            if os.path.exists(module_init_file):
                module_name = module_dir  # The directory name will be used as the module name
                plugin_class = load_plugin_class(f'{module_name}.{module_name}')

                if plugin_class and issubclass(plugin_class, FunctionPluginBase):
                    instance = plugin_class()
                    instance.initialize()  # Assuming initialize is required before starting
                    loaded_plugins.append(instance)
                    logging.info(f'Function Plugin {module_name} loaded successfully.')

    return loaded_plugins
