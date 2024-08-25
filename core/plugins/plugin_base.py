from core.logging.logger import Logger

class PluginBase:
    def __init__(self):
        self.app_logger = Logger.get_logger(self.__class__.__name__)

    def initialize(self, *args, **kwargs):
        """Common initialization logic for all plugins."""
        self.app_logger.info(f'Initializing {self.__class__.__name__}')
        self.on_initialize(*args, **kwargs)
        self.app_logger.info(f'{self.__class__.__name__} Initialized')

    def on_initialize(self, *args, **kwargs):
        """Plugin-specific initialization logic. Override in subclasses."""
        pass
