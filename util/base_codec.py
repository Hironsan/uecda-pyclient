# -*- coding: utf-8 -*-


class BaseEncoder(object):
    """
    データをサーバ/クライアントの形式から通信用の形式に変換する
    """
    def __init__(self, cards):
        self.table = self.to_table(cards)

    def to_table(self, cards):
        """
        Cardオブジェクトのリストを2次元配列に変換する
        ジョーカーの場所は前もって決めておく
        @return:
        """
        table = [[0] * 15 for i in range(8)]
        for card in cards:
            if card.is_joker():
                table[card.suit][card.rank] = 2
            else:
                table[card.suit][card.rank] = 1
        return table

    def get_table(self):
        return self.table


class BaseDecoder(object):
    """
    データを通信用の形式からサーバ/クライアント用の形式に変換する
    """
    def __init__(self, table, Card):
        self.cards = self.to_cards(table, Card)

    def to_cards(self, table, Card):
        """
        2次元配列をCardオブジェクトのリストに変換する
        @return:
        """
        cards = []
        for suit, line in enumerate(table[:5]):
            for rank, flag in enumerate(line):
                if flag < 1 or flag > 2:
                    continue
                cards.append(Card(rank, suit, flag))
        #cards.sort()
        return cards

    def get_cards(self):
        return self.cards