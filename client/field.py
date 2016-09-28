# -*- coding: utf-8 -*-


class Field(object):
    """
    場の状態を表すクラス
    """

    def __init__(self, table):
        self.is_exchange      = table[5][0]     # カード交換中か
        self.exchange_num     = table[5][1]     # カード交換の枚数
        self.is_my_turn       = table[5][2]     # 自分のターンか
        self.current_player   = table[5][3]     # 何番目のプレイヤーのターンか
        self.is_empty         = table[5][4]     # 場が流れたか
        self.is_11back        = table[5][5]     # イレブンバック発生中か
        self.is_kakumei       = table[5][6]     # 革命発生中か
        self.is_shibari       = table[5][7]     # 縛りが発生中か
        self.players_card_num = table[6][0:5]   # プレイヤーの手札枚数
        self.players_grade    = table[6][5:10]  # プレイヤーの階級
        self.players_seats    = [0] * 5         # プレイヤーの席番号
        for seat_id, player_id in enumerate(table[6][10:15]):
            self.players_seats[player_id] = seat_id

    def print_field_state(self):
        print 'is_exchange      =', self.is_exchange
        print 'exchange_num     =', self.exchange_num
        print 'is_my_turn       =', self.is_my_turn
        print 'current_player   =', self.current_player
        print 'is_empty         =', self.is_empty
        print 'is_11back        =', self.is_11back
        print 'is_kakumei       =', self.is_kakumei
        print 'is_shibari       =', self.is_shibari
        print 'players_card_num =', self.players_card_num
        print 'players_grade    =', self.players_grade
        print 'players_seats    =', self.players_seats