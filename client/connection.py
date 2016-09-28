# -*- coding: utf-8 -*-
import socket
import struct
from util.base_connection import BaseConnection


class Connection(BaseConnection):
    """
    通信用のクラス
    """
    def __init__(self, addr='127.0.0.1', port=42485):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.connect((addr, port))

    def recv_int(self):
        unpacked_value = self._recv_msg(byte_length=4)
        s = struct.Struct('!1I')
        integer = s.unpack(unpacked_value)
        return integer[0]

    # この中で、配列を構築すべきではない。構築する部分は分離して配列をsend_tableに渡すべき
    def send_name(self, name, protocol=20070):
        table = [[0] * 15 for i in range(8)]
        table[0][0] = protocol
        for i, ch in enumerate(name):
            table[1][i] = ord(ch)
        self.send_table(table)