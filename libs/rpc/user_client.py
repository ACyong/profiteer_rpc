# -*- coding: utf-8 -*-
from libs.rpc.base_client import BaseRPClient
from libs.rpc.user.user_thrift import user_thrift


class UserRPClient(BaseRPClient):
    """示例"""
    THRIFT_SERVICE = user_thrift.UserService
    RPC_SERVERS = ["127.0.0.1:5000", ]

    @classmethod
    def ping(cls):
        client = cls.get_rpc_client()
        return client.ping() == "pong"


print(UserRPClient.ping())
