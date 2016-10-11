# -*- coding: utf-8 -*-
import enum


class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __lt__(self, other):
        if self.rank < other.rank:
            return True
        if self.rank == other.rank and self.suit < other.suit:
            return True
        if other.is_joker():
            return True
        return False

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self):
        if self.is_joker():
            return self.suit.name
        return self.suit.name + self.rank.name

    def is_joker(self):
        return False


class Joker(Card):

    def is_joker(self):
        return True


class Rank(enum.IntEnum):
    Under = 0
    Three = 1
    Four = 2
    Five = 3
    Six = 4
    Seven = 5
    Eight = 6
    Nine = 7
    Ten = 8
    Jack = 9
    Queen = 10
    King = 11
    Ace = 12
    Two = 13
    Over = 14

    @property
    def name(self):
        if self.value == 12 or self.value == 13:
            return str(self.value - 11)
        elif self.value == 0 or self.value == 14:
            return str(self.value)
        else:
            return str(self.value + 2)


class Suit(enum.IntEnum):
    Null = 0
    S = 1
    D = 2
    H = 3
    C = 4
    X = 5
