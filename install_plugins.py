# Example usage
from core.plugins.plugin_installer import PluginInstaller
import jaydebeapi


if __name__ == "__main__":
    # Connect to H2 database
    conn = jaydebeapi.connect(
        "org.h2.Driver",
        "jdbc:h2:~/.flowforge/flowforge_db;MODE=MySQL;DB_CLOSE_ON_EXIT=FALSE",
        ["sa", ""],
        "D:/development/repos/gh/flowforge/h2/h2-2.3.232.jar"
    )

    installer = PluginInstaller(db_connection=conn)

    # Install a plugin
    installer.install_plugin('plugins/example_ui_plugin')

    # Load all installed plugins
    installed_plugins = installer.load_installed_plugins()
    print(installed_plugins)

    conn.close()
