import time
from core.plugins.function_plugin_base import FunctionPluginBase


class ExampleFunctionPlugin(FunctionPluginBase):
    def __init__(self):
        super().__init__()
        self.running = True  # A flag to control the running state

    def on_initialize(self, layout=None):
        """Plugin-specific initialization logic."""
        self.start()  # Start the thread when initialized

    def run(self):
        """Override the run method with the plugin's functionality."""
        self.app_logger.info("ExampleFunctionPlugin is running.")
        try:
            while self.running:
                self.app_logger.info("ExampleFunctionPlugin is working...")
                time.sleep(5)  # Simulate a task running in the background
        except Exception as e:
            self.app_logger.error(f"An error occurred: {e}")
        finally:
            self.app_logger.info("ExampleFunctionPlugin has stopped.")

    def stop(self):
        """Stop the plugin's thread gracefully."""
        self.running = False  # Set the running flag to False
        if self.thread.is_alive():
            self.thread.join()  # Wait for the thread to finish
        self.app_logger.info("ExampleFunctionPlugin stop method called.")
