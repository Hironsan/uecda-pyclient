# -*- coding: utf-8 -*-
import enum


class Players(object):
    """
    プレイヤーたちの状態を表すクラス
    """

    def __init__(self, data):
        self._current_player = data[5][3]        # 何番目のプレイヤーのターンか
        self._is_empty       = bool(data[5][4])  # 場が流れたか
        self._card_num       = data[6][0:5]      # プレイヤーの手札枚数
        self._class          = data[6][5:10]     # プレイヤーの階級
        self._seats          = data[6][10:15]    # どこに誰が座っているか

    def __str__(self):
        s = """
        current_player: {}
        is_empty      : {}
        card_num      : {}
        class         : {}
        seats         : {}
        """.format(self._current_player,
                   self._is_empty, self._card_num, self._class, self._seats)
        return s


"""
class BasePlayer(object):

    def __init__(self):
        self._id = None
        self._class = None
        self._seat = None


class OtherPlayer(BasePlayer):

    def __init__(self):
        pass
"""


class Player(object):

    def __init__(self, data):
        self._is_exchange = bool(data[5][0])  # カード交換中か
        self._exchange_num = data[5][1]       # カード交換の枚数
        self._is_my_turn = bool(data[5][2])   # 自分のターンか

    def needs_exchange(self):
        return self._is_exchange and self._exchange_num > 0

    def can_submit(self):
        return self._is_my_turn


class Class(enum.IntEnum):
    Daihinmin = 0
    Hinmin = 1
    Hemin = 2
    Fugo = 3
    Daifugo = 4
