# -*- coding: utf-8 -*-


class Players(object):
    """
    プレイヤーたちの状態を表すクラス
    """

    def __init__(self, table):
        self.is_exchange    = table[5][0]     # カード交換中か
        self.exchange_num   = table[5][1]     # カード交換の枚数
        self.is_my_turn     = table[5][2]     # 自分のターンか
        self.current_player = table[5][3]     # 何番目のプレイヤーのターンか
        self.is_empty       = table[5][4]     # 場が流れたか
        self.card_num = table[6][0:5]    # プレイヤーの手札枚数
        self.grade    = table[6][5:10]   # プレイヤーの階級
        self.seats    = table[6][10:15]  # どこに誰が座っているか

    def print_field_state(self):
        print('is_exchange      = {}'.format(self.is_exchange))
        print('exchange_num     = {}'.format(self.exchange_num))
        print('is_my_turn       = {}'.format(self.is_my_turn))
        print('current_player   = {}'.format(self.current_player))
        print('is_empty         = {}'.format(self.is_empty))
        print('card_num = {}'.format(self.card_num))
        print('grade    = {}'.format(self.grade))
        print('seats    = {}'.format(self.seats))


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
        11Back : {0}
        Kakumei: {1}
        Shibari: {2}
        """.format(self._is_11back, self._is_kakumei, self._is_shibari)
        return s

    def is_forward(self):
        return self._is_11back == self._is_kakumei

    def is_shibari(self):
        return self._is_shibari
