from core.logging.logger import Logger


class PluginBase:

    def __init__(self):
        self.app_logger = Logger.get_logger("app_logger")

    def initialize(self):
        """Initialize the plugin. Override this in subclasses."""
        pass

