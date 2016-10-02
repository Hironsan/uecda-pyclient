# -*- coding: utf-8 -*-
from client.card import Suit


class CardState(object):
    """
    場のカード状態を表すクラス
    """
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        s = """
        card_num      : {0}
        is_joker_only : {1}
        is_kaidan     : {2}
        is_pair       : {3}
        max card      : {4}
        min card      : {5}
        suits         : {6}
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
        return len(self.cards) == 1 and self.cards[0].suit == Suit.J

    def _is_same_suit(self):
        return len(set(card.suit for card in self.cards)) == 1

    def _is_same_rank(self):
        return len(set(card.rank for card in self.cards)) == 1
