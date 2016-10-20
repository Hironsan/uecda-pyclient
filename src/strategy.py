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

    def discard_le(self, melds, rank):
        """
        指定値以下のカードを捨てる
        """
        melds = [meld for meld in melds if meld[0].rank > rank]
        return melds

    def discard_ge(self, rank):
        """
        指定値以上のカードを捨てる
        """
        pass

    def discard_suit(self, suits):
        """
        指定スート以外のカードを捨てる
        """
        pass


class ExchangeStrategy(BaseStrategy):
    """
    カードの交換戦略を実装するクラス
    """

    def select_cards(self):
        cards = self._hand.get_lower()
        return cards


class FollowStrategy(BaseStrategy):

    def select_cards(self):
        if self._table_cards.is_kaidan():
            kaidans = self._hand.find_kaidans()
            if kaidans.get(self._table_cards.card_num(), None):
                kaidans = self.discard_le(kaidans[self._table_cards.card_num()], self._table_cards.max_card().rank)
                return kaidans[0] if kaidans else []

        if self._table_cards.is_pair():
            pairs = self._hand.find_groups()
            if pairs.get(self._table_cards.card_num(), None):
                pairs = self.discard_le(pairs[self._table_cards.card_num()], self._table_cards.max_card().rank)
                for cards in pairs:
                    print(' '.join(str(card) for card in cards))
                return pairs[0] if pairs else []

        return []


class LeadStrategy(BaseStrategy):

    def select_cards(self):
        kaidans = self._hand.find_kaidans()

        if len(kaidans) != 0:
            max_card_num = min(kaidans)
            return kaidans[max_card_num][0]

        pairs = self._hand.find_groups()
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