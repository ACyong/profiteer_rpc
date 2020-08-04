# -*- coding: utf-8 -*-
import os

import thriftpy2

path = os.path.join(os.path.dirname(__file__), "user.thrift")
print(path)
user_thrift = thriftpy2.load(path, module_name="user_thrift")
