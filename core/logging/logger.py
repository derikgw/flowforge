import logging.config
import yaml
import os

class Logger:
    _loggers = {}

    @staticmethod
    def load_config(config_file=None):
        if config_file is None:
            # Dynamically determine the config file path relative to PROJECT_ROOT
            project_root = os.getenv('PROJECT_ROOT', '')
            config_file = os.path.join(project_root, 'config', 'logger_config.yaml')

        # Ensure the logs directory exists
        logs_dir = os.path.join(os.getenv('PROJECT_ROOT', ''), 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

    @classmethod
    def get_logger(cls, name=__name__):
        if name in cls._loggers:
            return cls._loggers[name]
        else:
            # Load the logger configuration from YAML if it hasn't been done already
            if not logging.getLogger().hasHandlers():
                cls.load_config()

            # Retrieve or create the logger
            logger = logging.getLogger(name)
            cls._loggers[name] = logger
            return logger
