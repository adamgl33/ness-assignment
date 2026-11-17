import logging
import os
import sys
from datetime import datetime
from typing import Dict

from src.utils.Utils import sanitize_filename
from src.utils.config import get_logger_default_name, get_test_name, get_logger_level, get_logger_dir


class TestLogger:
    def __init__(self, config: Dict):
        self._test_name = get_test_name(config)
        self._logger_name = get_logger_default_name(config)
        self._level = get_logger_level(config)
        self.log_file = None
        self.logger = self._setup_logger(config)

    def _setup_logger(self, config: Dict) -> logging.Logger:
        """
        setup logger to output to file and stdout for CI
        """
        # create logger directory
        log_dir = get_logger_dir(config)
        os.makedirs(log_dir, exist_ok=True)

        # configure filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/{timestamp}_{sanitize_filename(self._test_name)}.log"
        self.log_file = log_file

        # config logger
        logger = logging.getLogger(self._logger_name)
        logger.setLevel(self._level)

        # prevent duplicate handlers
        if logger.handlers:
            logger.handlers.clear()

        # log format
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%H:%M:%S",
        )

        # file handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # stdout handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # prevent root logger duplicate writes
        logger.propagate = False

        return logger

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)


def get_default_logger(config: Dict) -> logging.Logger:
    name = get_logger_default_name(config)
    return logging.getLogger(name)


