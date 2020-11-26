# -*- coding: utf-8 -*-
import pytest

from config.config import CURRENT_ENV
from libs.pg.client import engine
from app.user.models.base import Base
from app.user.models.set_up import set_up_models


@pytest.fixture(scope="session", autouse=True)
def init_tables():
    if not CURRENT_ENV == 'Local':
        raise Exception("当前环境不能进行测试")

    set_up_models()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # 单元测试结束时删除所有表
    # yield
    # Base.metadata.drop_all(engine)
