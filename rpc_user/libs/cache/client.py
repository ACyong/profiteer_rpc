# -*- coding:utf-8 -*-
import redis

from rpc_user.config.config import REDIS_URI, REDIS_TIMEOUT, \
    REDIS_CONNECT_TIMEOUT, REDIS_POOL_SIZE

connection_pool = redis.ConnectionPool.from_url(REDIS_URI)
cache = redis.Redis(connection_pool=connection_pool,
                    socket_timeout=REDIS_TIMEOUT,
                    socket_connect_timeout=REDIS_CONNECT_TIMEOUT,
                    max_connections=REDIS_POOL_SIZE)
