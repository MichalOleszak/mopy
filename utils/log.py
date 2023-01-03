"""
Custom logging utility that automatically adds timestamp and logging level.
Example usage:
from utils.log import logger
logger.debug("Testing stuff")
logger.info("Hello")
logger.warning("Whoops!")
logger.error("Uh-oh...")
"""
import logging


def get_logger() -> logging.Logger:
    l = logging.getLogger("default")
    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s [%(process)d][%(filename)s:%(lineno)+3s]: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    l.setLevel(logging.DEBUG)
    if l.hasHandlers():
        l.handlers.clear()
    l.addHandler(handler)
    l.propagate = False
    return l


logger = get_logger()
