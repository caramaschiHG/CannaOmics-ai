"""Logging configuration using loguru."""

import logging
import sys

from loguru import logger


def setup_logging(level: str = "INFO", log_file: str = None):
    """
    Configure the Loguru logger.

    Parameters
    ----------
    level : str, optional
        Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
    log_file : str, optional
        Path to a file for saving logs.
    """
    # Remove default handler
    logger.remove()

    # Add stdout handler with rich-compatible formatting
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )

    # Optionally add file handler
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation="10 MB",
        )

    # Intercept standard logging messages
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def get_logger(name: str):
    """
    Get a pre-configured logger instance.

    Parameters
    ----------
    name : str
        Module or component name.

    Returns
    -------
    logger
        Loguru logger bound with the given name.
    """
    return logger.bind(name=name)
