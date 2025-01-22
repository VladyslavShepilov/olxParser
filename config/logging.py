import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except KeyError:
            level = record.levelno

        logger.log(level, record.getMessage())


def setup_logging():
    logger.remove()  # Remove default Loguru handler
    logger.add(
        "logs/{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        level="INFO",
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
