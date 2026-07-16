import logging
import sys

import structlog
from structlog.types import Processor

from dronzer.core.config import settings


def configure_logging() -> None:
    """Configures structured logging for the entire gateway."""

    # If testing, do not clutter output unless verbose
    if settings.ENVIRONMENT == "testing":
        structlog.configure(
            processors=[structlog.processors.JSONRenderer()],
            logger_factory=structlog.ReturnLoggerFactory(),
        )
        return

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.LOG_FORMAT == "JSON":
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Intercept standard logging and route to structlog
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer()
            if settings.LOG_FORMAT == "JSON"
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Suppress noisy external libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)
