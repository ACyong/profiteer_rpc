# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import random  # NOQA E402
import gevent  # NOQA E402
import thriftpy2  # NOQA E402
from thriftpy2.rpc import make_client  # NOQA E402


class BaseRPClient(object):
    THRIFT_SERVICE = None
    RPC_SERVERS = None
    RPC_INDEX = 0
    RPC_CONNS = {}
    TIMER = None

    @classmethod
    def __init_conn(cls, address):
        """真实建立tcp链接，并放入类缓存"""
        if not cls.THRIFT_SERVICE:
            raise Exception("子类必须写明具体服务名称")

        # TODO: log info before
        host, port = address.split(":")
        conn = make_client(cls.THRIFT_SERVICE, host, int(port))
        # TODO: log info after
        cls.RPC_CONNS[address] = conn
        return conn

    @classmethod
    def __get_rpc_client_with_cache(cls, address):
        """从类缓存获取链接，无则新建"""
        if address not in cls.RPC_CONNS:
            return cls.__init_conn(address)
        return cls.RPC_CONNS[address]

    @classmethod
    def __revival(cls, address):
        """探活链接，替换坏死链接
        Warning：协程spawn调用我
        """
        response = ""
        try:
            conn = cls.__get_rpc_client_with_cache(address)
            response = conn.ping()
        except Exception as e:
            # TODO: 换成打日志 log warn, not error
            print(e)

        if response != "pong":
            # TODO: log warn，体现出是复活坏死链接
            cls.__init_conn(address)

    @classmethod
    def _start_timer(cls, self):
        """定时器，周期探活、修复坏死链接"""
        while True:
            # 17--21秒
            how_long = random.randint(16, 22)
            gevent.sleep(how_long)
            check_jobs = [gevent.spawn(cls.__revival, address)
                          for address in cls.RPC_SERVERS]
            gevent.joinall(check_jobs, timeout=2, raise_error=False)

    @classmethod
    def get_rpc_client(cls, index=None):
        """对外暴露接口，调用我获取链接"""
        if isinstance(cls.RPC_SERVERS, list) or not cls.RPC_SERVERS:
            raise Exception("子类必须写明服务地址列表")

        if index is None:
            address = cls.RPC_SERVERS[cls.RPC_INDEX]
            cls.RPC_INDEX = (cls.RPC_INDEX + 1) % len(cls.RPC_SERVERS)
        else:
            if 0 <= index < len(cls.RPC_SERVERS):
                address = cls.RPC_SERVERS[index]
            else:
                raise Exception("请检查rpc client下标参数.")
        if not cls.TIMER:
            cls.TIMER = gevent.spawn(cls._start_timer)

        return cls.__get_rpc_client_with_cache(address)
