import importlib
import logging
import os
import yaml


def load_plugin_class(module_name):
    # Determine the directory and manifest path
    module_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules', module_name)
    manifest_file = os.path.join(module_dir, 'manifest.yaml')

    class_name = None
    script_name = None

    # Load the class name and script name from the manifest if it exists
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r') as f:
            manifest = yaml.safe_load(f)
            class_name = manifest.get('class_name')
            script_name = manifest.get('script_name')

    # If no manifest or script_name, derive the script name from the module name
    if not script_name:
        script_name = module_name

    # If no class_name, derive the class name from the module name
    if not class_name:
        class_name = ''.join([part.capitalize() for part in module_name.split('.')[-1].split('_')])

    # Attempt to import the correct script file within the module directory
    try:
        module = importlib.import_module(f'modules.{module_name}.{script_name}')
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
