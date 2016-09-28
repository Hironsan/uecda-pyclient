# -*- coding: utf-8 -*-


class Card(object):
    """
    1枚のカードを表す基底クラス
    ランク3には数字の1, ランク4には2...ランク2には13と対応させている
    """
    def __init__(self, rank, suit, flag):
        self.rank = rank
        self.suit = suit
        self._is_joker = True if flag == 2 else False

    def __cmp__(self, other):
        if self.is_joker() and other.is_joker():
            return 0
        if self.is_joker():
            return 1
        if other.is_joker():
            return -1
        if self.rank < other.rank:
            return -1
        elif self.rank == other.rank:
            if self.suit < other.suit:
                return -1
            elif self.suit == other.suit:
                return 0
            else:
                return 1
        elif self.rank > other.rank:
            return 1

    def __str__(self):
        suit_conv = {0: 's', 1: 'h', 2: 'd', 3: 'c'}
        if self.is_joker():
            return "JOKER"
        if self.rank <= 11:  # キング以下
            return "%s%d" % (suit_conv[self.suit], self.rank + 2)
        if self.rank <= 13:  # 2以下
            return "%s%d" % (suit_conv[self.suit], self.rank - 11)

    def is_joker(self):
        return self._is_joker


class Suit(object):
    """
    スートを表すクラス
    """
    def __init__(self, suit):
        """
        define as follows:
        spade=0, diamond=1, heart=2, club=3
        """
        self._suit = suit

    def get_suit(self):
        return self._suit

    def is_spade(self):
        return self._suit == 0

    def is_diamond(self):
        return self._suit == 1

    def is_heart(self):
        return self._suit == 2

    def is_club(self):
        return self._suit == 3

    def __cmp__(self, other):
        if self._suit < other.get_suit():
            return 1
        elif self._suit == other.get_suit():
            return 0
        else:
            return -1

    def __str__(self):
        if self.is_spade():
            return 's'
        if self.is_diamond():
            return 'd'
        if self.is_heart():
            return 'h'
        if self.is_club():
            return 'c'
        return 'JOKER'


class Rank(object):
    def __init__(self, rank):
        self._rank = rank

    def get_rank(self):
        return self._rank

    def __cmp__(self, other):
        if self._rank < other.get_rank():
            return -1
        elif self._rank == other.get_rank():
            return 0
        else:
            return 1

    def __str__(self):
        return str(self._rank)
