# -*- coding:utf-8 -*-
import pymongo

from rpc_user.config.config import MONGO_URI, MONGO_CONNECT_TIMEOUT, \
    MONGO_TIMEOUT, MONGO_POOL_SIZE

mongo = pymongo.MongoClient(MONGO_URI,
                            maxPoolSize=MONGO_POOL_SIZE,
                            connectTimeoutMS=MONGO_CONNECT_TIMEOUT,
                            socketTimeoutMS=MONGO_TIMEOUT,
                            connect=False)
