# -*- coding:utf-8 -*-
import os
from configparser import ConfigParser

try:
    CONFIG_PATH = os.environ.get('PROFITEER_CONFIG_PATH')
except Exception:
    raise ValueError


config = ConfigParser()
config.read(CONFIG_PATH)

# PG
DATABASE_URI = config.get(str("PG"), str("DATABASE_URI"))
print(DATABASE_URI)
