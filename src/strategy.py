# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class StrategyFactory(object):
    """
    Strategyを生成するFactory
    以下のような感じで使う。
    >>> factory = StrategyFactory()
    >>> strategy = factory.create(hand, table_effect, table_cards)
    >>> cards = strategy.select_cards()
    """
    def __init__(self, hand, table_effect, table_cards):
        self._hand = hand
        self._table_effect = table_effect
        self._table_cards = table_cards

    def create(self):
        if self._table_cards.card_num() == 0:
            return LeadStrategy(self._hand, self._table_effect, self._table_cards)
        else:
            return FollowStrategy(self._hand, self._table_effect, self._table_cards)


class BaseStrategy(ABC):
    """
    Strategyの抽象クラス
    """

    def __init__(self, hand, table_effect, table_cards):
        self._hand = hand
        self._table_effect = table_effect
        self._table_cards = table_cards

    @abstractmethod
    def select_cards(self):
        pass


class ExchangeStrategy(BaseStrategy):
    """
    カードの交換戦略を実装するクラス
    """

    def select_cards(self):
        cards = self._hand.get_lower()
        return cards


class ForwardStrategy(BaseStrategy):
    """
    カードの強さが逆転していない時の戦略を実装するクラス
    """

    def select_cards(self):
        if self._table_cards.is_kaidan():
            kaidans = self._hand.find_kaidans()
            if kaidans.get(self._table_cards.card_num, None):
                return kaidans[self._table_cards.card_num][-1]

        if self._table_cards.is_pair():
            pairs = self._hand.find_pairs()
            if pairs.get(self._table_cards.card_num, None):
                return pairs[self._table_cards.card_num][-1]

        return []


class FollowStrategy(BaseStrategy):

    def select_cards(self):
        if self._table_cards.is_kaidan():
            kaidans = self._hand.find_kaidans(joker=self._hand.has_joker())
            if kaidans.get(self._table_cards.card_num(), None):
                return kaidans[self._table_cards.card_num()][0]

        if self._table_cards.is_pair():
            pairs = self._hand.find_pairs(joker=self._hand.has_joker())
            if pairs.get(self._table_cards.card_num(), None):
                return pairs[self._table_cards.card_num()][0]

        return []


class LeadStrategy(BaseStrategy):

    def select_cards(self):
        kaidans = self._hand.find_kaidans(joker=self._hand.has_joker())

        if len(kaidans) != 0:
            max_card_num = min(kaidans)
            return kaidans[max_card_num][0]

        pairs = self._hand.find_pairs(joker=self._hand.has_joker())
        if len(pairs) != 0:
            max_card_num = min(pairs)
            return pairs[max_card_num][0]

        return []


class SequenceStrategy(BaseStrategy):

    def select_cards(self):
        pass


class GroupStrategy(BaseStrategy):

    def select_cards(self):
        pass


class ReverseStrategy(BaseStrategy):
    """
    カードの強さが逆転している時の戦略を実装するクラス
    """

    def select_cards(self):
        pass
