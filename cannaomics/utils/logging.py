"""Logging configuration using loguru."""

from __future__ import annotations

import logging
import sys

from loguru import logger

_CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

_FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level: <8} | "
    "{name}:{function}:{line} - "
    "{message}"
)


def setup_logging(level: str = "INFO", log_file: str | None = None) -> None:
    """Configure the Loguru logger.

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
        format=_CONSOLE_FORMAT,
        level=level,
        colorize=True,
    )

    # Optionally add file handler
    if log_file:
        logger.add(
            log_file,
            format=_FILE_FORMAT,
            level=level,
            rotation="10 MB",
        )

    # Intercept standard logging messages
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists
            try:
                level_name: str | int = logger.level(record.levelname).name
            except ValueError:
                level_name = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back  # type: ignore[assignment]
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level_name, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def get_logger(name: str):
    """Get a pre-configured logger instance.

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
