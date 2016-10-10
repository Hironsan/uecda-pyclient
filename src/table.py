# -*- coding: utf-8 -*-


class Table(object):
    pass


class TableEffect(object):
    """
    場にかかっている効果を表すクラス
    """

    def __init__(self, data):
        self._is_11back  = bool(data[5][5])  # イレブンバック発生中か
        self._is_kakumei = bool(data[5][6])  # 革命発生中か
        self._is_shibari = bool(data[5][7])  # 縛りが発生中か

    def __str__(self):
        s = """
        11Back : {}
        Kakumei: {}
        Shibari: {}
        """.format(self._is_11back, self._is_kakumei, self._is_shibari)
        return s

    def is_forward(self):
        return self._is_11back == self._is_kakumei

    def is_shibari(self):
        return self._is_shibari
