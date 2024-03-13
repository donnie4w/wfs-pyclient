"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/wfs-pyclient
"""
import _thread
import random
import ssl
import threading
import time

from thrift.protocol import *
from thrift.transport import *
from thrift.transport.TSSLSocket import TSSLSocket
from WfsIface import *

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


class WfsClient:
    transport = None
    conn = None
    host = ""
    port = 0
    tls = False
    name = ""
    pwd = ""
    connid = 0
    pingNum = 1
    lock = threading.Lock()

    def __init__(self):
        self.timeout = 60 * 1000

    def __connect(self) -> WfsAck:
        try:
            if self.tls:
                socket = TSSLSocket(self.host, self.port, cert_reqs=ssl.CERT_NONE)
            else:
                socket = TSocket.TSocket(self.host, self.port)
            socket.setTimeout(self.timeout)
            self.transport = TTransport.TBufferedTransport(socket)
            protocol = TCompactProtocol.TCompactProtocol(self.transport)
            self.conn = Client(protocol)
            logging.debug("conn>>" + str(self.pingNum))
            self.transport.open()
            self.pingNum = 0
            return self.Auth()
        except Exception as e:
            logging.error("connect error:" + str(e))

    def close(self) -> None:
        self.connid += 1
        self.transport.close()

    def setTimeout(self, timeout):
        self.timeout = timeout

    def newConnect(self, tls, host, port, name, pwd) -> WfsAck:
        self.tls, self.host, self.port, self.name, self.pwd = tls, host, port, name, pwd
        self.connid += 1
        ack = self.__connect()
        _thread.start_new_thread(self.timer, (self.connid,))
        return ack

    def reconnect(self):
        logging.warning("reconnect")
        if self.conn is not None:
            try:
                self.transport.close()
            except Exception as e:
                pass
        self.newConnect(self.tls, self.host, self.port, self.name, self.pwd)

    def Auth(self) -> WfsAck:
        wa = WfsAuth(name=self.name, pwd=self.pwd)
        with self.lock:
            return self.conn.Auth(wa)

    def ping(self) -> int:
        with self.lock:
            return self.conn.Ping()

    def timer(self, id):
        while id == self.connid:
            time.sleep(3)
            try:
                self.pingNum += 1
                p = self.ping()
                if p == 1:
                    self.pingNum -= 1
            except Exception as e:
                print("ping error:" + str(e))
            if self.pingNum > 5 and id == self.connid:
                self.reconnect()

    def Append(self, wf):
        with self.lock:
            return self.conn.Append(wf)

    def Delete(self, path):
        with self.lock:
            return self.conn.Delete(path)

    def Get(self, path):
        with self.lock:
            return self.conn.Get(path)

    def Rename(self,path,newPath):
        with self.lock:
            return self.conn.Rename(path,newPath)
