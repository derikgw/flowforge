import importlib
import logging
import os
from core.plugin_base import PluginBase


def load_modules(layout):
    modules_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modules')
    for filename in os.listdir(modules_dir):
        # Skip __init__.py files
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Strip off '.py'
            try:
                module = importlib.import_module(f'modules.{module_name}')
                class_name = ''.join([part.capitalize() for part in module_name.split('_')])
                print(f"Attempting to load {class_name} from {module_name}")

                if hasattr(module, class_name):
                    plugin_class = getattr(module, class_name)
                    print(f"Found class: {plugin_class}")

                    if issubclass(plugin_class, PluginBase):
                        instance = plugin_class()
                        layout.addWidget(instance.get_widget())
                        logging.info(f'Module {module_name} loaded successfully.')
                    else:
                        logging.warning(f'{class_name} is not a subclass of PluginBase.')
                else:
                    logging.warning(f'Class {class_name} not found in module {module_name}.')
            except ImportError as e:
                logging.error(f'Failed to import module {module_name}: {e}')
            except Exception as e:
                logging.error(f'Error loading module {module_name}: {e}')
