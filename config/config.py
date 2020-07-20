# -*- coding:utf-8 -*-
import os
from configparser import ConfigParser

try:
    CONFIG_PATH = os.environ.get('PROFITEER_CONFIG_PATH')
except Exception:
    raise ValueError


config = ConfigParser()
config.read(CONFIG_PATH)

# ENV
ENV = config["ENV"]
CURRENT_ENV = ENV.get("CURRENT_ENV")

# PG
PG = config["PG"]
PG_POOL_SIZE = PG.get("PG_POOL_SIZE")
PG_MAX_OVER = PG.get("PG_MAX_OVER")
PG_POOL_RECYCLE = PG.get("PG_POOL_RECYCLE")
PG_POOL_TIMEOUT = PG.get("PG_POOL_TIMEOUT")
PG_URI = PG.get("PG_URI")


# MongoDB
MONGO = config["MONGO"]
MONGO_POOL_SIZE = MONGO.get("MONGO_POOL_SIZE")
MONGO_TIMEOUT = MONGO.get("MONGO_TIMEOUT")
MONGO_CONNECT_TIMEOUT = MONGO.get("MONGO_CONNECT_TIMEOUT")
MONGO_URI = MONGO.get("MONGO_MAIN_URI")


# Redis
REDIS = config["REDIS"]
REDIS_POOL_SIZE = REDIS.get("REDIS_POOL_SIZE")
REDIS_TIMEOUT = REDIS.get("REDIS_TIMEOUT")
REDIS_CONNECT_TIMEOUT = REDIS.get("REDIS_CONNECT_TIMEOUT")
REDIS_URI = REDIS.get("REDIS_URI")
