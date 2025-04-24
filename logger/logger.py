import logging
from logging.handlers import RotatingFileHandler
from threading import Lock


class Logger:
    """Singleton logger with optional rotating file handler."""

    _instance = None
    _lock = Lock()

    LOG_LEVELS = {
        0: logging.NOTSET,
        5: logging.DEBUG,
        4: logging.INFO,
        3: logging.WARNING,
        2: logging.ERROR,
        1: logging.CRITICAL,
    }

    def __new__(cls, name=__name__, level=2, file_path=None, max_bytes=5*1024*1024, backup_count=5):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, name=__name__, level=2, file_path=None, max_bytes=5*1024*1024, backup_count=5):
        if self._initialized:
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LOG_LEVELS.get(level, logging.INFO))

        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(module)s - %(funcName)s | %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Rotating file handler
        if file_path:
            file_handler = RotatingFileHandler(
                file_path, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setLevel(self.LOG_LEVELS.get(level, logging.INFO))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self._initialized = True

    def get_logger(self):
        return self.logger
