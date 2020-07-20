# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String
from models.base import Base


class User(object):
    # 用来存储表名与对应orm model
    _mapper = {}

    @classmethod
    def model(cls, user_id):
        table_index = "{:0>2}".format(str(user_id)[-2:])
        class_name = 'User_{}'.format(table_index)
        ModelClass = cls._mapper.get(class_name)
        if ModelClass is not None:
            return ModelClass
        # 构建根据用户ID分表后各个表的orm model
        # type一个参数返回对象类型， 三个参数返回一个新的类型对象
        # type(name: 类名, bases: 父类， 基类, 类的属性及方法字典)
        ModelClass = type(class_name, (Base,), {
            '__module__': __name__,
            '__name__': class_name,
            '__tablename__': 'user_{}'.format(table_index),
            'id': Column(Integer, primary_key=True, autoincrement=True),
            'password': Column(String(256)),
            'state': Column(SmallInteger, default=0),
            'create_time': Column(DateTime, default=datetime.now),
            'update_time': Column(DateTime, default=datetime.now),
        })
        cls._mapper[class_name] = ModelClass
        return ModelClass
