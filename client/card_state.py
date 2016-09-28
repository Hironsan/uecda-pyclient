# -*- coding: utf-8 -*-


class CardState(object):
    """
    場のカード状態を表すクラス
    """
    def __init__(self, cards):
        self.card_num      = len(cards)
        self.is_joker_only = self._is_joker_only(cards)
        self.is_kaidan     = self._is_kaidan(cards)
        self.is_pair       = self._is_pair(cards)
        self.max_rank      = self._get_max_rank(cards)
        self.min_rank      = self._get_min_rank(cards)
        self.suit          = self._get_suit(cards)

    def _get_min_rank(self, cards):
        return cards[0].rank if len(cards) > 0 else -1

    def _get_max_rank(self, cards):
        return cards[-1].rank if len(cards) > 0 else -1

    def _get_suit(self, cards):
        suit = [False] * 5  # スペード、ハート、ダイヤ、クラブ、ジョーカーの順
        for card in cards:
            suit[card.suit] = True
        return suit

    def _is_pair(self, cards):
        return len(cards) >= 1 and self._is_same_rank(cards)

    def _is_kaidan(self, cards):
        return len(cards) >= 3 and self._is_same_suit(cards)

    def _is_joker_only(self, cards):
        return len(cards) == 1 and cards[0].is_joker()

    def _is_same_suit(self, cards):
        return len(set(card.suit for card in cards)) == 1

    def _is_same_rank(self, cards):
        return len(set(card.rank for card in cards)) == 1

    def print_card_state(self):
        print('card_num      = {}'.format(self.card_num))
        print('is_joker_only = {}'.format(self.is_joker_only))
        print('is_kaidan     = {}'.format(self.is_kaidan))
        print('is_pair       = {}'.format(self.is_pair))
        print('max_card      = {}'.format(self.max_rank))
        print('min_card      = {}'.format(self.min_rank))
        print('suit          = {}'.format(self.suit))
