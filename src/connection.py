# -*- coding: utf-8 -*-
import socket
import struct
import signal
signal.signal(signal.SIGPIPE, signal.SIG_IGN)


class Connection(object):
    """
    サーバとの通信用クラス
    """

    BINARY_INT = '!1I'
    BINARY_TABLE = '!120I'

    def __init__(self, addr='127.0.0.1', port=42485):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.connect((addr, port))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.sock.close()

    def recv_int(self):
        unpacked_value = self._recv_msg(byte_length=4)
        s = struct.Struct(self.BINARY_INT)
        integer = s.unpack(unpacked_value)
        return integer[0]

    def recv_table(self):
        unpacked_value = self._recv_msg(byte_length=480)
        s = struct.Struct(self.BINARY_TABLE)
        ls = s.unpack(unpacked_value)
        table = [ls[15 * i: 15 * (i + 1)][:] for i in range(8)]  # 8x15のリストに変換
        return table

    def _recv_msg(self, byte_length):
        unpacked_data = b''
        while len(unpacked_data) < byte_length:
            chunk = self.sock.recv(byte_length - len(unpacked_data), 0)
            if chunk == '':
                raise RuntimeError('socket connection broken')
            unpacked_data += chunk
        return unpacked_data

    # この中で、配列を構築すべきではない。構築する部分は分離して配列をsend_tableに渡すべき
    def send_name(self, name, protocol=20070):
        table = [[0] * 15 for i in range(8)]
        table[0][0] = protocol
        for i, ch in enumerate(name):
            table[1][i] = ord(ch)
        self.send_table(table)

    def send_table(self, table):
        ls = [item for inner in table for item in inner]  # 2次元リストを1次元に変換
        s = struct.Struct(self.BINARY_TABLE)
        packed_value = s.pack(*ls)
        self._send_msg(packed_value)

    def _send_msg(self, msg):
        self.sock.sendall(msg)
