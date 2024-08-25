import os
import logging
from core.plugins.ui_plugin_base import UIPluginBase
from core.plugins.menu_plugin_base import MenuPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class


def load_ui_plugins(layout):
    modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')

    for module_dir in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_dir)
        if os.path.isdir(module_path):
            module_init_file = os.path.join(module_path, '__init__.py')
            if os.path.exists(module_init_file):
                plugin_class = load_plugin_class(module_dir)  # Use the directory name as the module name

                if plugin_class:
                    if issubclass(plugin_class, UIPluginBase):
                        instance = plugin_class()
                        instance.initialize(layout)
                        widget = instance.get_widget()
                        if widget:
                            layout.addWidget(widget)
                        logging.info(f'UI Plugin {module_dir} loaded successfully.')

                    elif issubclass(plugin_class, MenuPluginBase):
                        instance = plugin_class()
                        instance.initialize(layout)
                        logging.info(f'Menu Plugin {module_dir} loaded successfully.')
