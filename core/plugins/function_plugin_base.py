import threading
from core.plugins.plugin_base import PluginBase
from core.logging.logger import Logger


class FunctionPluginBase(PluginBase):
    def __init__(self):
        super().__init__()
        self.thread = None

    def start(self):
        """Start the plugin's functionality in a separate thread."""
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            self.app_logger.info(f"{self.__class__.__name__} started in a new thread.")

    def run(self):
        """Override this method with the plugin's functionality."""
        raise NotImplementedError("Subclasses should implement this method.")

    def stop(self):
        """Override this method to stop the plugin if necessary."""
        self.app_logger.info(f"{self.__class__.__name__} stop method called.")
        pass
