import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.plugins.function_plugin_base import FunctionPluginBase
from core.events.event_bus import event_bus


class PathMonitorHandler(FileSystemEventHandler):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def on_modified(self, event):
        if event.is_directory:
            return
        self.logger.info(f"File modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory:
            return
        self.logger.info(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.logger.info(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return
        self.logger.info(f"File moved: from {event.src_path} to {event.dest_path}")


class PathMonitor(FunctionPluginBase):
    def __init__(self, folder_to_monitor=None):
        super().__init__()
        # Use a default path if none is provided
        self.folder_to_monitor = folder_to_monitor or "default/path/to/monitor"
        self.observer = None
        self.running = False

        # Register for the update_monitored_path event
        event_bus.register("update_monitored_path", self.update_monitored_path)

    def on_initialize(self):
        """Plugin-specific initialization logic."""
        self.app_logger.info(f"Initializing PathMonitor for folder: {self.folder_to_monitor}")
        self.start_monitoring()

    def start_monitoring(self):
        """Start the folder monitoring."""
        if not os.path.exists(self.folder_to_monitor):
            self.app_logger.error(f"Directory does not exist: {self.folder_to_monitor}")
            return

        if self.observer:
            self.stop_monitoring()

        event_handler = PathMonitorHandler(self.app_logger)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.folder_to_monitor, recursive=True)
        self.observer.start()
        self.running = True
        self.app_logger.info(f"Started monitoring folder: {self.folder_to_monitor}")

    def stop_monitoring(self):
        """Stop the folder monitoring."""
        if self.observer and self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False
            self.observer = None  # Reset observer
            self.app_logger.info(f"Stopped monitoring folder: {self.folder_to_monitor}")

    def run(self):
        """Keep the thread alive while monitoring."""
        self.app_logger.info("PathMonitor thread running...")
        while self.running:
            try:
                self.observer.join(1)
            except Exception as e:
                self.app_logger.error(f"Error in PathMonitorPlugin: {e}")

    def stop(self):
        """Stop the observer when the plugin stops."""
        self.stop_monitoring()
        self.app_logger.info("PathMonitor stopped.")

    def update_monitored_path(self, new_folder):
        """Update the folder to be monitored."""
        self.app_logger.info(f"Updating monitored folder to: {new_folder}")
        self.stop_monitoring()
        self.folder_to_monitor = new_folder
        self.start_monitoring()
