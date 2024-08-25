# Temporary test to directly load the classes
from modules.example_function_plugin.example_function_plugin import ExampleFunctionPlugin
from modules.example_ui_plugin.example_ui_plugin import ExampleUiPlugin
from modules.main_menu.main_menu import MainMenu

# Create instances to ensure they can be loaded
example_function_plugin_instance = ExampleFunctionPlugin()
example_ui_plugin_instance = ExampleUiPlugin()
main_menu_instance = MainMenu()

print("All plugins loaded successfully.")
