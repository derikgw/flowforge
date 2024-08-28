import os
from PyQt5.QtWidgets import (
    QMainWindow, QToolBar, QToolButton, QAction, QDockWidget, QLabel, QMenu, QTabWidget, QVBoxLayout, QWidget,
    QMessageBox, QApplication
)
from PyQt5.QtCore import Qt

from core.logging.logger import Logger
from core.plugins.plugin_manager import PluginManager
from core.plugins.ui.plugins_view import PluginsView
from core.ui.styles import apply_theme


class MainWindow(QMainWindow):
    def __init__(self, plugin_manager: PluginManager):
        super().__init__()
        self.plugin_manager = plugin_manager
        self.app_logger = Logger.get_logger("app_logger")

        self.setWindowTitle("FlowForge")
        self.setGeometry(100, 100, 1280, 720)

        # Create the ribbon toolbar
        self.toolbar = QToolBar("Ribbon", self)
        self.toolbar.setMovable(False)
        self.toolbar.setAllowedAreas(Qt.TopToolBarArea)
        self.toolbar.setFixedHeight(40)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # File dropdown in toolbar
        file_button = QToolButton(self)
        file_button.setText("File")
        file_button.setPopupMode(QToolButton.InstantPopup)

        file_menu = QMenu(file_button)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        file_button.setMenu(file_menu)
        self.toolbar.addWidget(file_button)

        # Views dropdown in toolbar
        views_button = QToolButton(self)
        views_button.setText("Views")
        views_button.setPopupMode(QToolButton.InstantPopup)

        views_menu = QMenu(views_button)
        views_button.setMenu(views_menu)
        self.toolbar.addWidget(views_button)

        # Plugins dropdown in toolbar
        plugins_button = QToolButton(self)
        plugins_button.setText("Plugins")
        plugins_button.setPopupMode(QToolButton.InstantPopup)

        plugins_menu = QMenu(plugins_button)
        plugins_button.setMenu(plugins_menu)
        self.toolbar.addWidget(plugins_button)

        # Example actions for the toolbar
        dark_action = QAction("Dark", self)
        light_action = QAction("Light", self)
        dark_action.triggered.connect(lambda: self.set_theme("dark"))
        light_action.triggered.connect(lambda: self.set_theme("light"))
        self.toolbar.addAction(dark_action)
        self.toolbar.addAction(light_action)

        # Initialize the tab widget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Add the Plugins View tab
        self.plugins_view = PluginsView(self.plugin_manager)
        plugins_tab = QWidget()
        plugins_layout = QVBoxLayout(plugins_tab)
        plugins_layout.addWidget(self.plugins_view)
        self.tab_widget.addTab(plugins_tab, "Plugins")

        # Populate the views menu with available plugins
        self.add_plugins_to_views(views_menu)
        self.add_plugins_to_plugins_menu(plugins_menu)

        # Register for the shutdown event
        QApplication.instance().aboutToQuit.connect(self.handle_shutdown)

        # Hide the default QMenuBar
        self.menuBar().setVisible(False)

    def add_plugins_to_views(self, views_menu):
        """Add plugins to the Views menu."""
        for plugin in self.plugin_manager.get_plugins_by_type("UI"):
            plugin_name = plugin.get_name()
            plugin_action = QAction(plugin_name, self)
            plugin_action.triggered.connect(lambda p=plugin: self.set_central_widget(p))
            views_menu.addAction(plugin_action)

    def add_plugins_to_plugins_menu(self, plugins_menu):
        """Add plugins to the Plugins menu."""
        for plugin in self.plugin_manager.get_plugins_by_type("UI"):
            plugin_name = plugin.get_name()
            install_action = QAction(f"Install {plugin_name}", self)
            install_action.triggered.connect(lambda p=plugin_name: self.install_plugin(p))
            plugins_menu.addAction(install_action)

    def set_central_widget(self, plugin):
        """Set the central widget to the selected plugin's widget."""
        widget = plugin.get_widget()
        if widget:
            current_widget = self.tab_widget.currentWidget()
            if current_widget is not None:
                current_widget.setParent(None)
            self.tab_widget.addTab(widget, plugin.get_name())
            self.tab_widget.setCurrentWidget(widget)

    def install_plugin(self, plugin_name):
        """Install the selected plugin."""
        try:
            plugin_directory = os.path.join(self.plugin_manager.plugins_directory, plugin_name)
            self.plugin_manager.install_plugin(plugin_name, plugin_directory)
            self.app_logger.info(f"Plugin {plugin_name} installed successfully.")
            self.plugins_view.refresh_plugins()  # Refresh the Plugins View
        except Exception as e:
            self.app_logger.error(f"Failed to install plugin {plugin_name}: {e}")

    def set_theme(self, theme):
        """Set the application theme."""
        if theme in ["dark", "light"]:
            self.app_logger.info(f"Applying {theme} theme.")
            QApplication.setOverrideCursor(Qt.WaitCursor)
            QApplication.processEvents()
            self.setUpdatesEnabled(False)
            apply_theme(QApplication.instance(), theme)
            self.setUpdatesEnabled(True)
            QApplication.restoreOverrideCursor()
            self.repaint()
        else:
            self.app_logger.warning(f"Unknown theme: {theme}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.app_logger.info("Initiating application shutdown.")
            try:
                self.plugin_manager.stop_all_plugins()
                self.app_logger.info("All plugins stopped successfully.")
            except Exception as e:
                self.app_logger.error(f"Error during plugin shutdown: {e}")

            try:
                self.save_current_session()
                self.app_logger.info("Session saved successfully.")
            except Exception as e:
                self.app_logger.error(f"Error saving session state: {e}")

            event.accept()
            self.app_logger.info("Application shutdown complete.")
        else:
            event.ignore()

    def save_current_session(self):
        """Save the current session layout to a file."""
        # Implement session saving logic here
        pass

    def handle_shutdown(self):
        """Handle application shutdown."""
        self.app_logger.info("Application is shutting down.")
        self.plugin_manager.stop_all_plugins()
