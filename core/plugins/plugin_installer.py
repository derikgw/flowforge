import os
import json
import subprocess
import jaydebeapi
from core.logging.logger import Logger


class PluginInstaller:
    def __init__(self, db_path):
        self.logger = Logger.get_logger("app_logger")
        self.db_path = db_path
        self.conn = self._connect_to_db()

    def _connect_to_db(self):
        """Establish a connection to the H2 database."""
        try:
            jar_path = os.path.join(os.environ['PROJECT_ROOT'], 'libs', 'h2-2.3.232.jar')  # Corrected jar path
            conn = jaydebeapi.connect(
                'org.h2.Driver',
                f'jdbc:h2:{self.db_path};AUTO_SERVER=TRUE',
                ['sa', ''],
                jar_path
            )
            return conn
        except Exception as e:
            self.logger.error(f"Failed to connect to the database: {e}")
            return None

    def _execute_query(self, query, params=None):
        """Helper function to execute SQL queries."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            self.logger.error(f"Database query failed: {e}")
            return None

    def is_plugin_registered(self, plugin_name):
        """Check if the plugin is registered in the database."""
        query = "SELECT COUNT(*) FROM plugins WHERE name = ?"
        cursor = self._execute_query(query, [plugin_name])
        if cursor:
            count = cursor.fetchone()[0]
            return count > 0
        return False

    def install_plugin(self, plugin_name, plugin_path):
        """Install a plugin by creating its virtual environment and registering it in the database."""
        try:
            with open(os.path.join(plugin_path, 'plugin.json'), 'r') as f:
                plugin_config = json.load(f)

            # Create a virtual environment for the plugin
            venv_path = os.path.join(plugin_path, '.venv')
            subprocess.check_call(['python', '-m', 'venv', venv_path])

            pip_executable = os.path.join(venv_path, 'Scripts', 'pip')
            for dependency in plugin_config.get('dependencies', []):
                subprocess.check_call([pip_executable, 'install', dependency])

            # Prepare and execute the SQL query to register the plugin
            query = """
                INSERT INTO plugins (name, version, description, entry_point, type, path, communication_protocol)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = [
                plugin_config['name'],
                plugin_config['version'],
                plugin_config['description'],
                plugin_config['entry_point'],
                plugin_config['type'],
                plugin_path,
                plugin_config['communication_protocol']
            ]
            cursor = self._execute_query(query, params)

            if cursor:
                self.conn.commit()  # Commit the transaction
                self.logger.info(f"Plugin {plugin_name} registered in the database successfully.")
            else:
                self.logger.error(f"Failed to register plugin {plugin_name} in the database.")

        except Exception as e:
            self.logger.error(f"Failed to install plugin {plugin_name}: {e}")

    def uninstall_plugin(self, plugin_name):
        """Uninstall a plugin by removing it from the database."""
        try:
            query = "SELECT path FROM plugins WHERE name = ?"
            cursor = self._execute_query(query, [plugin_name])
            plugin_path = cursor.fetchone()[0]

            venv_path = os.path.join(plugin_path, '.venv')
            if os.path.exists(venv_path):
                subprocess.check_call(['rm', '-rf', venv_path])

            query = "DELETE FROM plugins WHERE name = ?"
            self._execute_query(query, [plugin_name])
            self.conn.commit()

            self.logger.info(f"Plugin {plugin_name} uninstalled successfully.")
        except Exception as e:
            self.logger.error(f"Failed to uninstall plugin {plugin_name}: {e}")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
