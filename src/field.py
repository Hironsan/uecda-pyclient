# -*- coding: utf-8 -*-


class Players(object):
    """
    プレイヤーたちの状態を表すクラス
    """

    def __init__(self, table):
        self.is_exchange    = bool(table[5][0])  # カード交換中か
        self.exchange_num   = table[5][1]        # カード交換の枚数
        self.is_my_turn     = bool(table[5][2])  # 自分のターンか
        self.current_player = table[5][3]        # 何番目のプレイヤーのターンか
        self.is_empty       = bool(table[5][4])  # 場が流れたか
        self.card_num       = table[6][0:5]      # プレイヤーの手札枚数
        self.grade          = table[6][5:10]     # プレイヤーの階級
        self.seats          = table[6][10:15]    # どこに誰が座っているか

    def __str__(self):
        s = """
        is_exchange   : {}
        exchange_num  : {}
        is_my_turn    : {}
        current_player: {}
        is_empty      : {}
        card_num      : {}
        grade         : {}
        seats         : {}
        """.format(self.is_exchange, self.exchange_num, self.is_my_turn, self.current_player,
                   self.is_empty, self.card_num, self.grade, self.seats)
        return s


class FieldEffect(object):
    """
    場にかかっている効果を表すクラス
    """

    def __init__(self, table):
        self._is_11back  = bool(table[5][5])  # イレブンバック発生中か
        self._is_kakumei = bool(table[5][6])  # 革命発生中か
        self._is_shibari = bool(table[5][7])  # 縛りが発生中か

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
