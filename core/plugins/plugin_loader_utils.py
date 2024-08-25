import importlib
import logging


def load_plugin_class(module_name, modules_dir='modules'):
    """
    Load the plugin class from a module.

    :param module_name: The name of the module (without the .py extension).
    :param modules_dir: The directory where modules are located.
    :return: The plugin class, or None if not found.
    """
    try:
        module = importlib.import_module(f'{modules_dir}.{module_name}')
        class_name = ''.join([part.capitalize() for part in module_name.split('_')])

        if hasattr(module, class_name):
            plugin_class = getattr(module, class_name)
            return plugin_class
        else:
            logging.warning(f'Class {class_name} not found in module {module_name}.')
            return None
    except ImportError as e:
        logging.error(f'Failed to import module {module_name}: {e}')
        return None
    except Exception as e:
        logging.error(f'Error loading module {module_name}: {e}')
        return None
