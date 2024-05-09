# Create a logger for deropy with colors

import logging
loggers = []


def init_logger(name):
    if name in loggers:
        return

    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.ERROR)


def change_logger_level(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
