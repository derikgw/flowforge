from PyQt5.QtWidgets import QWidget


class PluginBase:
    def __init__(self):
        self.widget = None

    def get_widget(self):
        return self.widget

    def add_functionality(self, main_window):
        pass

    def add_to_menu_bar(self, menu_bar):
        pass
