# -*- coding: utf-8 -*-
from .cards import CardSetFactory


class Hand(object):
    """
    手札を表すクラス
    """
    def __init__(self, card_table):
        factory = CardSetFactory(card_table)
        self.__cards = factory.create()

    def __str__(self):
        return ' '.join(str(card) for card in self.__cards)

    def __getattr__(self, name):
        return getattr(self.__cards, name)
