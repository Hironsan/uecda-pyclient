# -*- coding: utf-8 -*-


class BaseField(object):
    """
    場の状態を保持し、操作するためのクラス
    """

    def __init__(self):
        self._is_11back  = False        # イレブンバック中か
        self._is_shibari = False        # 場がマークで縛られているか
        self._is_kakumei = False        # 革命中か

    def is_11back(self):
        return self._is_11back

    def is_shibari(self):
        return self._is_shibari

    def is_kakumei(self):
        return self._is_kakumei

    def is_reverse(self):
        return self._is_kakumei ^ self._is_11back

    def print_state(self):
        print("is_11back  = {}".format(self.is_11back)
        print("is_shibari = {}".format(self.is_shibari)
        print("is_kakumei = {}".format(self.is_kakumei)
