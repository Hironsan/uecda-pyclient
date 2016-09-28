# -*- coding: utf-8 -*-
class Cards(object):

    def __init__(self):
        self.cards = []

    def __str__(self):
        self.cards.sort()
        return ' '.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def set_card(self, card):
        self.cards.append(card)

    def get_min_rank(self, cards):
        return cards[0].rank if len(cards) > 0 else -1

    def get_max_rank(self, cards):
        return cards[-1].rank if len(cards) > 0 else -1

    def get_suits(self, cards):
        suits = [False] * 5  # スペード、ハート、ダイヤ、クラブ、ジョーカーの順
        for card in cards:
            suits[card.suit] = True
        return suits

    def is_pair(self, cards):
        return len(cards) >= 1 and self._are_same_rank(cards)

    def is_kaidan(self, cards):
        return len(cards) >= 3 and self._are_same_suit(cards)

    def is_joker_only(self, cards):
        return len(cards) == 1 and cards[0].is_joker()

    def _are_same_suit(self, cards):
        return len(set(card.suit for card in cards)) == 1

    def _are_same_rank(self, cards):
        return len(set(card.rank for card in cards)) == 1