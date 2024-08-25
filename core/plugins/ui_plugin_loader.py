import os
import logging
from core.plugins.ui_plugin_base import UIPluginBase
from core.plugins.menu_plugin_base import MenuPluginBase
from core.plugins.plugin_loader_utils import load_plugin_class


def load_ui_plugins(layout):
    modules_dir = os.path.join(os.getenv('PROJECT_ROOT'), 'modules')
    for filename in os.listdir(modules_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Strip off '.py'
            plugin_class = load_plugin_class(module_name)

            if plugin_class:
                if issubclass(plugin_class, UIPluginBase):
                    instance = plugin_class()
                    instance.initialize(layout)
                    widget = instance.get_widget()
                    if widget:
                        layout.addWidget(widget)
                    logging.info(f'UI Plugin {module_name} loaded successfully.')

                elif issubclass(plugin_class, MenuPluginBase):
                    instance = plugin_class()
                    instance.initialize(layout)
                    logging.info(f'Menu Plugin {module_name} loaded successfully.')
