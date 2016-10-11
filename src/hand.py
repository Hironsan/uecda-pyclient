# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import combinations

from .card import Card, Joker, Suit, Rank


class Hand(object):
    """
    手札を表すクラス
    """
    def __init__(self, cards):
        self.cards = self._encode(cards)

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def find_kaidans(self):
        """
        あり得る階段を生成
        階段は階段の枚数ごとにまとめる.
        @return:
        """
        # 先頭カードを選んで、そこから何枚カードが連続するかを返す関数
        # 枚数を返してもらえれば、その範囲を選択してappendできる
        kaidans_grouped_by_card_num = defaultdict(list)
        for cards in self.group_by_suit().values():   # スートごとにまとめたカードを
            for idx, start_card in enumerate(cards):  # 階段の先頭カードをstart_cardとして
                kaidan = [start_card]
                for jdx, next_card in enumerate(cards[idx+1:], 1):  # 隣のカードをnext_cardとして
                    if start_card.rank + jdx != next_card.rank:    # ランクが異なる場合は
                        break                                      # それ以降は続かない
                    kaidan.append(next_card)
                    if len(kaidan) >= 3:                           # 枚数が3枚以上だったら
                        kaidans_grouped_by_card_num[len(kaidan)].append(kaidan[:])

        return kaidans_grouped_by_card_num

    def find_pairs(self):
        """
        あり得るペアを生成
        ペアはペアの枚数ごとにまとめる.
        cards_grouped_by_card_num = {1: [(card), (card)],
                                     2: [(card, card), (card, card),...],
                                     ...
                                     }
        @return: 枚数ごとにまとめられたペアの辞書
        """
        pairs_grouped_by_card_num = defaultdict(list)
        for cards in self.group_by_rank().values():               # ランクごとにまとめたカードを
            for card_num in range(1, len(cards)+1):               # card_numはペアの枚数
                for comb_cards in combinations(cards, card_num):  # card_num枚で組み合わせを生成
                    pairs_grouped_by_card_num[len(comb_cards)].append(comb_cards)

        return pairs_grouped_by_card_num

    def group_by_rank(self):
        """
        同ランクのカードをまとめる
        """
        cards_grouped_by_rank = defaultdict(list)
        for card in self.cards:
            if card.is_joker():
                continue
            cards_grouped_by_rank[card.rank].append(card)

        return cards_grouped_by_rank

    def group_by_suit(self):
        """
        同スートのカードをまとめる
        """
        cards_grouped_by_suit = defaultdict(list)
        for card in self.cards:
            if card.is_joker():
                continue
            cards_grouped_by_suit[card.suit].append(card)

        return cards_grouped_by_suit

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
