import logging
from rich.logging import RichHandler

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with rich coloured output.

    Args:
        name: logger name, typically __name___

    Returns:
        configure logger instance
    """
    logging.basicConfig(
        level = logging.INFO,
        format = "%(message)s",
        datefmt = "[%X]",
        handlers = [RichHandler(rich_tracebacks= True)]
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
    logging.getLogger("datasets").setLevel(logging.WARNING)

    return logging.getLogger(name)