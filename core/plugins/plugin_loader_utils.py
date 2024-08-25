import importlib
import logging
import os
import yaml


def load_plugin_class(module_name):
    # Determine the directory and manifest path
    module_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules', module_name)
    manifest_file = os.path.join(module_dir, 'plugin_manifest.yaml')

    class_name = None

    # Load the class name from the manifest if it exists
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r') as f:
            manifest = yaml.safe_load(f)
            class_name = manifest.get('class_name')

    # If no manifest or class_name, derive the class name from the module name
    if not class_name:
        class_name = ''.join([part.capitalize() for part in module_name.split('.')[-1].split('_')])

    # Attempt to import the correct script file within the module directory
    try:
        module = importlib.import_module(f'modules.{module_name}.{module_name}')
        logging.info(f'Module loaded: {module}')
        if hasattr(module, class_name):
            return getattr(module, class_name)
        else:
            logging.warning(
                f'Class {class_name} not found in module {module_name}. Available attributes: {dir(module)}')
    except ImportError as e:
        logging.error(f'Failed to import module {module_name}: {e}')
    except Exception as e:
        logging.error(f'Error loading module {module_name}: {e}')
    return None
