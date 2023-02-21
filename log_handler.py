import logging
import os
import sys

from time import perf_counter
from enum import Enum

absolute_path = os.path.dirname(__file__)

os.makedirs(os.path.join(absolute_path, 'logs'), exist_ok=True)

LOG_FORMATTER = "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
LOG_FILE = os.path.join(absolute_path, 'logs/main_log.txt')


class Logger(logging.getLoggerClass()):
    """Handles logging to the file and stroudt with timestamps."""
    def __init__(self, name: str):
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = logging.FileHandler(
            filename=LOG_FILE, mode='a')
        self.fmt = LOG_FORMATTER
        self.stdout_handler.setFormatter(logging.Formatter(LOG_FORMATTER))
        self.file_handler.setFormatter(logging.Formatter(LOG_FORMATTER))
        self.addHandler(self.stdout_handler)
        self.addHandler(self.file_handler)


class LogTemplates(Enum):
    """Storing log templates for the split_image.py"""
    STARTED = "Started to create frames for {} image sets."
    FRAMES_CREATED = "Successfully created {} frames."
    VIDEO_CREATED = "Successfully created the videofile."
    RUNTIME = "The function was executed in {run_time:.6f} seconds."
    BAD_SET_NUMBER = "The number of sets should be in range (1, 90)."
    NO_DATASET = "Unable to find DAVIS dataset with corresponding "\
        "file structure in the script directory."

    def format(self, *args, **kwargs):
        return self.value.format(*args, **kwargs)

    def __str__(self):
        return self.value


def runtime(function: callable) -> callable:
    """Measures precise time of the function runtime and writes it into
    the main log."""
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = function(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time

        logger = Logger(__name__)
        logger.info(LogTemplates.RUNTIME.format(run_time=run_time))
        return result
    return wrapper
