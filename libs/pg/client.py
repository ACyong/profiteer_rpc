# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config.config import PG_URI, PG_POOL_SIZE, PG_MAX_OVER, PG_POOL_RECYCLE, \
    PG_POOL_TIMEOUT

engine = create_engine(
    PG_URI,
    pool_size=PG_POOL_SIZE,
    max_overflow=PG_MAX_OVER,
    pool_recycle=PG_POOL_RECYCLE,
    pool_timeout=PG_POOL_TIMEOUT)


def get_user_session():
    return scoped_session(sessionmaker(bind=engine))()
