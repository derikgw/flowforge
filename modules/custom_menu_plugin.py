# modules/custom_menu_plugin.py
from PyQt5.QtWidgets import QAction
from core.plugins.menu_plugin_base import MenuPluginBase


class CustomMenuPlugin(MenuPluginBase):
    def add_to_menu_bar(self, menu_bar):
        custom_action = QAction("Custom Action", menu_bar)
        custom_action.triggered.connect(self.custom_action_triggered)

        # Find the MainMenu instance and add the custom action
        for menu in menu_bar.actions():
            if menu.menu().title() == "File":
                menu.menu().addAction(custom_action)

    def custom_action_triggered(self):
        print("Custom Action triggered!")
        # Implement the custom action logic here
