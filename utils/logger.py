# -*- coding: utf-8 -*-
import atexit
import logging
from logging.handlers import MemoryHandler


LOGGING_MSG_FORMAT = '%(asctime)s %(levelname)s %(module)s.py ' \
                     'line:%(lineno)d %(message)s'

logger = logging.getLogger()


def set_up_logger(log_level=logging.DEBUG):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
    memory_handler = MemoryHandler(
        capacity=64,
        flushLevel=logging.ERROR,
        target=stream_handler
    )
    memory_handler.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
    logger.setLevel(log_level)
    logger.addHandler(memory_handler)

    def flush():
        memory_handler.flush()
    atexit.register(flush)
    logger.debug("Logger init")
