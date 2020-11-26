# -*- coding: utf-8 -*-
import atexit
import logging
from logging.handlers import MemoryHandler

from config.config import CURRENT_ENV

LOGGING_MSG_FORMAT = '%(asctime)s %(levelname)s %(module)s.py ' \
                     'line:%(lineno)d %(message)s'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logger = logging.getLogger()


def set_up_logger(log_level=logging.DEBUG):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(logging.Formatter(fmt=LOGGING_MSG_FORMAT,
                                                  datefmt=LOGGING_DATE_FORMAT))
    logger.setLevel(log_level)
    if CURRENT_ENV != 'Product':
        logger.addHandler(stream_handler)
        return

    memory_handler = MemoryHandler(
        capacity=64,
        flushLevel=logging.ERROR,
        target=stream_handler
    )
    memory_handler.setFormatter(logging.Formatter(fmt=LOGGING_MSG_FORMAT,
                                                  datefmt=LOGGING_DATE_FORMAT))
    logger.addHandler(memory_handler)

    def flush():
        memory_handler.flush()
    atexit.register(flush)
    logger.debug("Logger init")
