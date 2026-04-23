import logging
import sys


from constants import __app_name__


logger = logging.getLogger(__app_name__)


def setup_logger(logger_name: str = ""):
    """
    Sets up a logger with a specific name and configuration.

    This function initializes and configures a logger instance with a provided name.
    The logger is configured to stream messages to the standard output using a specific
    log format. Useful for consistent logging across various modules.

    :param logger_name: The name of the logger to set up. If not provided, the root logger is used.
    :type logger_name: str
    :return: A configured logger instance.
    :rtype: logging.Logger
    """
    log_formatter = logging.Formatter(
        "%(asctime)s |%(levelname)s|%(funcName)s:%(lineno)d| %(message)s"
    )
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_formatter)

    logger_edit = logging.getLogger(logger_name)
    logger_edit.addHandler(log_handler)
