# -*- coding: utf-8 -*-
from thriftpy2.rpc import make_client

from utils.logger import logger


class BaseRPClient(object):
    THRIFT_SERVICE = None
    RPC_SERVERS = None
    RPC_INDEX = 0
    RPC_CONNS = {}

    @classmethod
    def _init_conn(cls, address):
        """真实建立tcp链接，并放入类缓存"""
        if not cls.THRIFT_SERVICE:
            raise Exception("子类必须写明具体服务名称")

        host, port = address.split(":")
        logger.info("{} {} start connect".format(
            cls.THRIFT_SERVICE, address))
        conn = make_client(cls.THRIFT_SERVICE, host, int(port))
        logger.info("{} {} connect success".format(
            cls.THRIFT_SERVICE, address))
        cls.RPC_CONNS[address] = conn
        return conn

    @classmethod
    def _get_rpc_client_with_cache(cls, address):
        """从类缓存获取链接，无则新建"""
        if address not in cls.RPC_CONNS:
            return cls._init_conn(address)
        return cls.RPC_CONNS[address]

    @classmethod
    def get_rpc_client(cls, index=None):
        """对外暴露接口，调用我获取链接"""
        if not isinstance(cls.RPC_SERVERS, list) or not cls.RPC_SERVERS:
            raise Exception("子类必须写明服务地址列表")

        if index is None:
            address = cls.RPC_SERVERS[cls.RPC_INDEX]
            cls.RPC_INDEX = (cls.RPC_INDEX + 1) % len(cls.RPC_SERVERS)
        else:
            if 0 <= index < len(cls.RPC_SERVERS):
                address = cls.RPC_SERVERS[index]
            else:
                raise Exception("请检查rpc client下标参数.")
        return cls._get_rpc_client_with_cache(address)

    @classmethod
    def _reconnect(cls, address):
        logger.info("Service reconnect: {}".format(address))
        try:
            cls._init_conn(address)
        except Exception as e:
            logger.info("Service reconnect: {} fail: {}".format(
                address, str(e)))

    @classmethod
    def _is_alive(cls, client):
        try:
            status = client.ping() == 'pong'
        except Exception as e:
            status = False
            logger.info("Service alive fail: {}".format(str(e)))
        return status

    @classmethod
    def keep_alive(cls):
        """对外暴露接口，调用我client保活"""
        if not cls.RPC_CONNS:
            return
        for address, conn in cls.RPC_CONNS.items():
            logger.info("Service {} start check".format(address))
            if not cls._is_alive(conn):
                cls._reconnect(address)
