# -*- coding: utf-8 -*-
from gevent.pool import Pool

from config.config import GEVENT_POOL_SIZE
from app.user.handlers.user import UserHandler


# GEVENT_POOL_SIZE 跟pg数据库 PG_POOL_SIZE 相同
pool = Pool(GEVENT_POOL_SIZE)
TimeoutLevel = 3


class Dispatcher(object):
    @classmethod
    def ping(cls):
        return "pong"

    @classmethod
    def createUser(cls, user):
        job = pool.spawn(UserHandler.create_user, user)
        job.join(timeout=TimeoutLevel)
