# -*- coding: utf-8 -*-
import pytest

from rpc_user.config.config import CURRENT_ENV
from rpc_user.libs.pg.client import engine
from rpc_user.models.base import Base
from rpc_user.models.set_up import set_up_models


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
