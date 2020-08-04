# -*- coding: utf-8 -*-
"""
压力测试
"""
import random

from gevent import monkey

monkey.patch_all()  # noqa

import gevent
from thriftpy2.rpc import make_client

from rpc_user.libs.rpc.user.user_thrift import user_thrift

qps = 0
fail = 0
size = 2  # client并发数


def init_clients(size):
    clients = list()
    for _ in range(size // 2):
        clients.append(make_client(
            user_thrift.UserService, '127.0.0.1', 9000))
        clients.append(make_client(
            user_thrift.UserService, '127.0.0.1', 9000))
    return clients


clients = init_clients(size)


def get_client():
    global clients
    return clients.pop()


def print_qps():
    global qps, fail
    times = 0
    total_qps = 0
    total_fail = 0
    while times <= 300:
        gevent.sleep(1)
        total_qps += qps
        total_fail += fail
        print("Current QPS:{}, FAIL:{}".format(qps, fail))
        qps = 0
        fail = 0
        times += 1
    print("5min, Total QPS:{}, Total Fail: {}".format(total_qps, total_fail))


def send_request(start, end):
    global qps, fail
    client = get_client()
    for user_id in range(start, end):
        try:
            payload = user_thrift.User(**{
                "id": user_id, "password": "123456", "state": 0})
            client.createUser(payload)
        except Exception as e:
            print("send_request fail: %s" % str(e))
            fail += 1
        qps += 1


if __name__ == "__main__":
    g1 = gevent.spawn(print_qps)
    gs = [g1]
    for i in range(size):
        g = gevent.spawn(send_request, i * 100000, (i + 1) * 100000)
        gs.append(g)
    gevent.joinall(gs)
