import logging
import logging.config
import os
import yaml


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

            # Create a unique logger for the plugin
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)  # Ensure the logger level is set to DEBUG

            # Create a file handler for the plugin's log file
            logs_dir = os.path.join(os.getenv('PROJECT_ROOT', ''), 'logs')
            log_file = os.path.join(logs_dir, f"{name}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf8')
            file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
            logger.addHandler(file_handler)

            # Optionally, also log to console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
            logger.addHandler(console_handler)

            cls._loggers[name] = logger
            return logger
