# -*- coding: utf-8 -*-
from gevent import monkey  # noqa

monkey.patch_all()  # noqa

from psycogreen.gevent import patch_psycopg  # noqa

patch_psycopg()  # noqa

import argparse
import warnings

from thriftpy2.protocol import TBinaryProtocolFactory
from thriftpy2.server import TThreadedServer
from thriftpy2.thrift import TApplicationException, TProcessor, TType
from thriftpy2.transport import (TBufferedTransportFactory, TServerSocket,
                                 TSSLServerSocket)

from dispacher import Dispatcher
from rpc_user.models.set_up import set_up_models
from rpc_user.utils.logger import logger, set_up_logger
from rpc_user.libs.rpc.user.user_thrift import user_thrift

# 初始化日志
set_up_logger()
# 初始化分表，防并发
set_up_models()


class _TProcessor(TProcessor):
    def process_in(self, iprot):
        api, type, seqid = iprot.read_message_begin()
        if api not in self._service.thrift_services:
            iprot.skip(TType.STRUCT)
            iprot.read_message_end()
            return api, seqid, TApplicationException(
                TApplicationException.UNKNOWN_METHOD), None  # noqa

        args = getattr(self._service, api + "_args")()
        args.read(iprot)
        iprot.read_message_end()
        result = getattr(self._service, api + "_result")()

        # convert kwargs to args
        api_args = [args.thrift_spec[k][1] for k in sorted(args.thrift_spec)]

        if api != 'ping':
            # get client IP address 为了拿到客户端连接的log，没啥好办法
            peername = iprot.trans.sock.getpeername()
            peername = peername if peername else ["unknown_ip", "unknown_port"]
            client_ip, client_port = peername
            logger.info("{}:{} {} {}".format(client_ip, client_port,
                                             api, args.__dict__))

        def call():
            f = getattr(self._handler, api)
            return f(*(args.__dict__[k] for k in api_args))

        return api, seqid, result, call


def _make_server(service, handler,
                 host="localhost", port=9090, unix_socket=None,
                 proto_factory=TBinaryProtocolFactory(),
                 trans_factory=TBufferedTransportFactory(),
                 client_timeout=3000, certfile=None):
    processor = _TProcessor(service, handler)

    if unix_socket:
        server_socket = TServerSocket(unix_socket=unix_socket)
        if certfile:
            warnings.warn("SSL only works with host:port, not unix_socket.")
    elif host and port:
        if certfile:
            server_socket = TSSLServerSocket(
                host=host, port=port, client_timeout=client_timeout,
                certfile=certfile)
        else:
            server_socket = TServerSocket(
                host=host, port=port, client_timeout=client_timeout)
    else:
        raise ValueError("Either host/port or unix_socket must be provided.")

    return TThreadedServer(processor, server_socket,
                           iprot_factory=proto_factory,
                           itrans_factory=trans_factory)


parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', help="server listen host")
parser.add_argument('-P', '--port', type=int, help="server listen port")

if __name__ == '__main__':
    args = parser.parse_args()
    if not args.host or not args.port:
        raise Exception("please enter host and port")
    server = _make_server(user_thrift.UserService, Dispatcher,
                          args.host, args.port, )
    server.serve()
