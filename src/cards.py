# -*- coding: utf-8 -*-
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


class CardSet(object):

    def __init__(self, card_table):
        self.cards = card_table

    def has_joker(self):
        return self.cards[4][1] == 2

    def create_kaidan_with_joker(self):
        tgt_cards = [[0] * 15 for i in range(8)]
        for i in range(4):
            count = 1
            no_j_count = 0
            for j in reversed(range(14)):
                if self.cards[i][j] == 1:
                    count += 1
                    no_j_count += 1
                else:
                    count = no_j_count + 1
                    no_j_count = 0
                if count >= 3:
                    tgt_cards[i][j] = count
                else:
                    tgt_cards[i][j] = 0
        return tgt_cards

    def create_kaidan(self):
        tgt_cards = [[0] * 15 for i in range(8)]
        for i in range(4):
            count = 0
            for j in reversed(range(15)):
                if self.cards[i][j] == 1:
                    count += 1
                else:
                    count = 0
                if count >= 3:
                    tgt_cards[i][j] = count
                else:
                    tgt_cards[i][j] = 0
        return tgt_cards

    def create_kaidan(self):
        tgt_cards = [[0] * 15 for i in range(8)]
        for s in range(4):
            for r in reversed(Rank):
                if self.cards[s][r] == 1:
                    tgt_cards[s][r] = tgt_cards[s][r + 1] + 1
        return tgt_cards

    def create_kaidan_with_joker(self):
        tgt_cards = [[0] * 15 for i in range(8)]
        for s in range(4):
            for r in reversed(Rank):
                if self.cards[s][r] == 1:
                    tgt_cards[s][r] = tgt_cards[s][r + 1] + 1
                else:
                    tgt_cards[s][r] = max(tgt_cards[s][r + 1], tgt_cards[s][r + 1] - 1)
        return tgt_cards

    def create_group(self):
        tgt_cards = [[0] * 15 for i in range(8)]
        for r in Rank:
            count = self.cards[0][r] + self.cards[1][r] + self.cards[2][r] + self.cards[3][r]
            for s in range(4):
                if self.cards[s][r] == 1:
                    tgt_cards[s][r] = count
        return tgt_cards

    def create_group_with_joker(self):
        tgt_cards = [[0] * 15 for i in range(8)]
        for r in Rank:
            count = self.cards[0][r] + self.cards[1][r] + self.cards[2][r] + self.cards[3][r] + 1
            for s in range(4):
                if self.cards[s][r] == 1:
                    tgt_cards[s][r] = count
        return tgt_cards

    def find_kaidans(self, joker):
        if joker:
            kaidans = self.create_kaidan_with_joker()
        else:
            kaidans = self.create_kaidan()
        kaidans_grouped_by_num = defaultdict(list)
        for i in range(4):
            for j in range(13):
                if kaidans[i][j] == 0:
                    continue
                cards = []
                for k in range(kaidans[i][j]):
                    if self.cards[i][j+k] == 1:
                        card = Card(Rank(j+k), Suit(i))
                    elif self.cards[i][j+k] == 0:
                        card = Joker(Rank(j+k), Suit(i))
                    cards.append(card)
                    if len(cards) >= 3:
                        kaidans_grouped_by_num[len(cards)].append(cards[:])

        return kaidans_grouped_by_num

    def find_groups(self, joker):
        if joker:
            groups = self.create_group_with_joker()
        else:
            groups = self.create_group()
        groups_by_num = defaultdict(list)
        for j in range(15):
            for i in range(4):
                if groups[i][j] == 0:
                    continue
                cards = []
                for k in range(groups[i][j]):
                    if i + k >= 5:
                        continue
                    if self.cards[i+k][j] == 1:
                        card = Card(Rank(j), Suit(i+k))
                    elif self.cards[i+k][j] == 0:
                        card = Joker(Rank(j), Suit(i+k))
                    cards.append(card)
                    groups_by_num[len(cards)].append(cards[:])
        return groups_by_num

    def get_lower(self, num=2):
        cards = []
        count = 0
        for j in range(15):
            for i in range(4):
                if count == num:
                    return cards
                if self.cards[i][j] == 1:
                    count += 1
                    cards.append(Card(Rank(j), Suit(j)))

    def discard_lt(self, rank):
        """
        指定値未満のカードを捨てる
        """
        pass

    def discard_le(self, rank):
        """
        指定値以下のカードを捨てる
        """
        for s in range(4):
            for r in Rank:
                if r > rank:
                    return
                self.cards[s][r] = 0

    def discard_gt(self, rank):
        """
        指定値より大きいカードを捨てる
        """
        pass

    def discard_ge(self, rank):
        """
        指定値以上のカードを捨てる
        """
        for s in range(4):
            for r in reversed(Rank):
                if r < rank:
                    return
                self.cards[s][r] = 0

    def discard_ne(self, rank):
        """
        指定値以外ののカードを捨てる
        """
        pass

    def discard_eq(self, rank):
        """
        指定値のカードを捨てる
        """
        pass

    def discard_suit(self, suit):
        """
        指定スート以外のカードを捨てる
        """
        pass
