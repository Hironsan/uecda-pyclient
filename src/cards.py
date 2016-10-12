# -*- coding: utf-8 -*-
from .card import Card, Joker, Rank, Suit


class TableCards(object):
    """
    場のカード状態を表すクラス
    """
    def __init__(self, cards):
        self.cards = self._encode(cards)

    def __str__(self):
        s = """
        card_num      : {}
        is_joker_only : {}
        is_kaidan     : {}
        is_pair       : {}
        max card      : {}
        min card      : {}
        suits         : {}
        """.format(self.card_num(), self.is_joker_only(), self.is_kaidan(),
                   self.is_pair(), self.max_card(), self.min_card(), self.suits())
        return s

    def card_num(self):
        return len(self.cards)

    def min_card(self):
        return self.cards[0] if len(self.cards) > 0 else []

    def max_card(self):
        return self.cards[-1] if len(self.cards) > 0 else []

    def suits(self):
        suits = set([card.suit for card in self.cards])
        suits = sum(suits)
        return suits

    def is_pair(self):
        return len(self.cards) >= 1 and self._is_same_rank()

    def is_kaidan(self):
        return len(self.cards) >= 3 and self._is_same_suit()

    def is_joker_only(self):
        return len(self.cards) == 1 and self.cards[0].is_joker()

    def _is_same_suit(self):
        return len(set(card.suit for card in self.cards)) == 1

    def _is_same_rank(self):
        return len(set(card.rank for card in self.cards)) == 1

    @classmethod
    def _decode(self, cards):
        """
        Cardオブジェクトのリストを2次元配列に変換する
        @return:
        """
        table = [[0] * 15 for i in range(8)]
        for card in cards:
            if card.is_joker():
                if len(cards) == 1:
                    table[0][0] = 2
                else:
                    table[card.suit.value][card.rank.value] = 2
            else:
                table[card.suit.value][card.rank.value] = 1
        return table

    def _encode(self, data):
        """
        2次元配列をCardオブジェクトのリストに変換する
        @return:
        """
        cards = []
        for suit, line in enumerate(data[:5]):
            for rank, flag in enumerate(line):
                if flag == 0:
                    continue
                elif flag == 1:
                    cards.append(Card(Rank(rank), Suit(suit)))
                elif flag == 2:
                    cards.append(Joker(Rank(rank), Suit(suit)))
                else:
                    print('Flag is not understood.')
                    raise
        cards.sort()
        return cards