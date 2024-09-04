from core.plugins.plugin_installer import PluginInstaller
import os

if __name__ == "__main__":
    # Set the database path
    db_path = os.path.expanduser("~/.flowforge/flowforge_db")

    # Initialize the PluginInstaller with the database path
    installer = PluginInstaller(db_path=db_path)

    # Install a plugin
    plugin_path = os.path.join('plugins', 'example_ui_plugin')
    installer.install_plugin('example_ui_plugin', plugin_path)

    # Load all installed plugins (implement this method if necessary in PluginInstaller)
    # installed_plugins = installer.load_installed_plugins()
    # print(installed_plugins)

    # Close the database connection
    installer.close()
