import importlib
import logging
import os
import yaml


def load_plugin_class(module_name, plugin_manager=None):
    module_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules', module_name)
    manifest_file = os.path.join(module_dir, 'manifest.yaml')

    class_name = None
    script_name = None
    dependencies = []

    if os.path.exists(manifest_file):
        with open(manifest_file, 'r') as f:
            manifest = yaml.safe_load(f)
            class_name = manifest.get('class_name')
            script_name = manifest.get('script_name')
            dependencies = manifest.get('dependencies', [])

    if not script_name:
        script_name = module_name

    if not class_name:
        class_name = ''.join([part.capitalize() for part in module_name.split('.')[-1].split('_')])

    try:
        module = importlib.import_module(f'modules.{module_name}.{script_name}')
        logging.info(f'Module loaded: {module}')

        if hasattr(module, class_name):
            plugin_class = getattr(module, class_name)

            # Resolve dependencies if any
            if plugin_manager and dependencies:
                resolved_dependencies = [
                    plugin_manager.get_plugin_instance(dep) for dep in dependencies
                ]
                return plugin_class, resolved_dependencies
            else:
                return plugin_class, []
        else:
            logging.warning(
                f'Class {class_name} not found in module {module_name}. Available attributes: {dir(module)}')
    except ImportError as e:
        logging.error(f'Failed to import module {module_name}: {e}')
    except Exception as e:
        logging.error(f'Error loading module {module_name}: {e}')
    return None, []
