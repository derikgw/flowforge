import importlib
import logging


def load_plugin_class(module_name):
    try:
        module = importlib.import_module(f'modules.{module_name}')
        # Capitalize each part of the module_name split by underscores
        class_name = ''.join([part.capitalize() for part in module_name.split('.')[-1].split('_')])
        if hasattr(module, class_name):
            return getattr(module, class_name)
        else:
            logging.warning(f'Class {class_name} not found in module {module_name}.')
    except ImportError as e:
        logging.error(f'Failed to import module {module_name}: {e}')
    except Exception as e:
        logging.error(f'Error loading module {module_name}: {e}')
    return None
