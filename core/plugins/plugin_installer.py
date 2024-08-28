import json
import subprocess
import os
import jaydebeapi


class PluginInstaller:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def install_plugin(self, plugin_dir):
        """Install a plugin from the given directory."""
        try:
            plugin_json_path = os.path.join(plugin_dir, 'plugin.json')
            with open(plugin_json_path, 'r') as f:
                plugin_info = json.load(f)

            # Install dependencies
            self._install_dependencies(plugin_info['dependencies'])

            # Register plugin in the H2 database
            self._register_plugin(plugin_info, plugin_dir)

            print(f"Plugin {plugin_info['name']} installed successfully.")
        except Exception as e:
            print(f"Failed to install plugin: {e}")

    def _install_dependencies(self, dependencies):
        """Install the plugin's dependencies using pip."""
        for dependency in dependencies:
            subprocess.check_call([os.sys.executable, "-m", "pip", "install", dependency])

    def _register_plugin(self, plugin_info, plugin_dir):
        """Register the plugin's metadata in the H2 database."""
        cursor = self.db_connection.cursor()

        # Ensure the plugins table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plugins (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                version VARCHAR(50),
                description TEXT,
                entry_point VARCHAR(255),
                type VARCHAR(50),
                path VARCHAR(255),
                communication_protocol VARCHAR(50)
            )
        ''')

        # Insert the plugin data into the table
        cursor.execute('''
            INSERT INTO plugins (name, version, description, entry_point, type, path, communication_protocol)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            plugin_info['name'],
            plugin_info['version'],
            plugin_info['description'],
            plugin_info['entry_point'],
            plugin_info['type'],
            plugin_dir,
            plugin_info['communication_protocol']
        ))

        self.db_connection.commit()
        cursor.close()

    def load_installed_plugins(self):
        """Load all installed plugins from the H2 database."""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM plugins')
        plugins = cursor.fetchall()
        cursor.close()
        return plugins