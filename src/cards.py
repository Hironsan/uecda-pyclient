# -*- coding: utf-8 -*-
from itertools import product, combinations
from collections import defaultdict
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


class CardSetFactory(object):

    def __init__(self, card_table):
        self.cards = card_table

    def create(self):
        if self.has_joker():
            return JokerCardSet(self.cards)
        else:
            return NormalCardSet(self.cards)

    def has_joker(self):
        return self.cards[4][1] == 2


class BaseCardSet(object):

    def __init__(self, card_table):
        self.cards = card_table

    def has_joker(self):
        return self.cards[4][1] == 2

    def create_card_table(self):
        return [[0] * len(Rank) for _ in Suit]

    def create_kaidan(self):
        pass

    def create_grouop(self):
        pass

    def discard_le(self, rank):
        """
        指定値以下のカードを捨てる
        """
        for s in Suit:
            for r in Rank:
                if r > rank:
                    return
                self.cards[s][r] = 0

    def discard_ge(self, rank):
        """
        指定値以上のカードを捨てる
        """
        for s in Suit:
            for r in reversed(Rank):
                if r < rank:
                    return
                self.cards[s][r] = 0

    def discard_suit(self, suits):
        """
        指定スート以外のカードを捨てる
        """
        for s in Suit:
            if s in suits:
                continue
            for r in Rank:
                self.cards[s][r] = 0

    def find_kaidans(self):
        kaidans = self.create_kaidan()
        kaidans_by_num = defaultdict(list)
        for s in Suit:
            for r in Rank:
                cards = []
                for dr in range(kaidans[s][r]):
                    if r + dr > Rank.Over:
                        break
                    if self.cards[s][r+dr] == 1:
                        card = Card(Rank(r+dr), Suit(s))
                    elif self.cards[s][r+dr] == 0:
                        card = Joker(Rank(r+dr), Suit(s))
                    cards.append(card)
                    if len(cards) >= 3:
                        kaidans_by_num[len(cards)].append(cards[:])

        return kaidans_by_num

    def get_lower(self, num=2):
        cards = []
        count = 0
        for r in Rank:
            for i in Suit:
                if count == num:
                    return cards
                if self.cards[i][r] == 1:
                    count += 1
                    cards.append(Card(r, Suit(i)))

        return cards


class NormalCardSet(BaseCardSet):

    def create_kaidan(self):
        cards = self.create_card_table()
        for s in Suit:
            for r in reversed(Rank):
                if self.cards[s][r] == 1:
                    cards[s][r] = cards[s][r + 1] + 1

        return cards

    def create_group(self):
        cards = self.create_card_table()
        for r in Rank:
            count = sum(self.cards[s][r] for s in Suit)
            for s in Suit:
                if self.cards[s][r] == 1:
                    cards[s][r] = count

        return cards

    def find_groups(self):
        groups_by_num = defaultdict(list)
        for prod in product((0, 1), repeat=len(Suit)):
            for r in Rank:
                vec = tuple([self.cards[s][r] for s in Suit])
                _and = [min(i, j) for i, j in zip(vec, prod)]
                cards = [Card(r, s) for s, el in zip(Suit, _and) if el == 1]
                if cards and cards not in groups_by_num[len(cards)]:
                    groups_by_num[len(cards)].append(cards)

        return groups_by_num


class JokerCardSet(BaseCardSet):

    def create_kaidan(self):
        cards = self.create_card_table()
        for s in Suit:
            count = 1
            no_j_count = 0
            for r in reversed(Rank):
                if self.cards[s][r] == 1:
                    count += 1
                    no_j_count += 1
                else:
                    count = no_j_count + 1
                    no_j_count = 0
                cards[s][r] = count

        return cards

    def create_group(self):
        cards = self.create_card_table()
        for r in Rank:
            count = sum(self.cards[s][r] for s in Suit) + 1
            for s in Suit:
                if self.cards[s][r] == 1:
                    cards[s][r] = count

        return cards

    def find_groups(self):
        groups_by_num = defaultdict(list)
        for prod in product((0, 1), repeat=len(Suit)):
            for r in Rank:
                vec = tuple([self.cards[s][r] for s in Suit])
                _and = [min(i, j) for i, j in zip(vec, prod)]
                _xor = [0 if i == j else 1 for i, j in zip(_and, prod)]
                if sum(_xor) == 1:  # Joker使って出せる場合
                    cards = [Card(r, s) for s, el in zip(Suit, _and) if el == 1] + [Joker(r, s) for s, el in zip(Suit, _xor) if el == 1]
                else:
                    cards = [Card(r, s) for s, el in zip(Suit, _and) if el == 1]
                if cards and cards not in groups_by_num[len(cards)]:
                    groups_by_num[len(cards)].append(cards)
        cards = [card for card in groups_by_num[1] if not card[0].is_joker()]
        cards.append([Joker(Rank(0), Suit(0))])
        groups_by_num[1] = cards

        return groups_by_num