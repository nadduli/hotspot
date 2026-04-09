"""Logging configuration for the entire application."""

import logging
import sys


def setup_logging(debug: bool = False) -> None:
    """
    Configure logging for the application.
    Call this once at startup in main.py.
    """
    log_level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Silence noisy third party loggers
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if debug else logging.WARNING
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)