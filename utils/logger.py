# nexus_ai/utils/logger.py

import logging
from datetime import datetime

def setup_logger(name="NexusLogger", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Example usage
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Logger initialized")
