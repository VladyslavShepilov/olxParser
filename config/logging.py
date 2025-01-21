import logging
from loguru import logger

def setup_logging():
    logger.remove()  # Remove default logger
    logger.add("logs/{time}.log", rotation="1 day", retention="7 days", compression="zip")
    logging.basicConfig(level=logging.INFO)
    logger.info("Logging setup completed.")

