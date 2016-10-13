# -*- coding: utf-8 -*-
from .cards import CardSet


class Hand(object):
    """
    手札を表すクラス
    """
    def __init__(self, card_table):
        self.cards = CardSet(card_table)

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def has_joker(self):
        return self.cards.has_joker()

    def find_kaidans(self, joker):
        """
        あり得る階段を生成
        階段は階段の枚数ごとにまとめる.
        @return:
        """
        kaidans_grouped_by_num = self.cards.find_kaidans(joker)

        return kaidans_grouped_by_num

    def find_pairs(self, joker):
        """
        あり得るペアを生成
        ペアはペアの枚数ごとにまとめる.
        cards_grouped_by_card_num = {1: [(card), (card)],
                                     2: [(card, card), (card, card),...],
                                     ...
                                     }
        @return: 枚数ごとにまとめられたペアの辞書
        """
        pairs_grouped_by_card_num = self.cards.find_groups(joker)
        return pairs_grouped_by_card_num

    def get_lower(self):
        return self.cards.get_lower()