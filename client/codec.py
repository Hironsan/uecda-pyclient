# -*- coding: utf-8 -*-
from .card import Card


class Encoder(object):
    """
    データをクライアントの形式から通信用の形式に変換する
    """
    def __init__(self):
        pass

    def to_table(self, cards):
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
                    table[card.suit][card.rank] = 2
            else:
                table[card.suit][card.rank] = 1
        return table


class Decoder(object):
    """
    データを通信用の形式からクライアント用の形式に変換する
    """
    def __init__(self):
        pass

    def to_cards(self, table):
        """
        2次元配列をCardオブジェクトのリストに変換する
        @return:
        """
        cards = []
        for suit, line in enumerate(table[:5]):
            for rank, flag in enumerate(line):
                if flag == 0:
                    continue
                cards.append(Card(rank, suit, flag))
        cards.sort()
        return cards


if __name__ == '__main__':
    L = [[0] * 15 for i in range(8)]
    L[0][1] = 1
    L[1][1] = 1
    L[2][1] = 1
    L[3][1] = 1
    #L[1][1] = 1
    L[0][2] = 1
    L[0][3] = 1
    L[0][4] = 1
    L[0][13] = 1
    L[4][1] = 2
    decoder = Decoder()
    cards = decoder.to_cards(L)
    from hand import Hand
    hand = Hand(cards)
    print("hand")
    print(hand)
    print()
    print("cards grouped by rank")
    for rank, cards in hand.group_by_rank().items():
        print(rank, ":",)
        for card in cards:
            print(card,)
        print()
    print()
    print("cards grouped by suit")
    for suit, cards in hand.group_by_suit().items():
        print(suit, ":",)
        for card in cards:
            print(card,)
        print()
    hand.generate_pairs()
    hand.generate_kaidans()
    #print " ".join(str(card) for card in cards)
    #cards.sort(reverse=True)
    #print " ".join(str(card) for card in cards)
    #from card_state import CardState
    #state = CardState(cards)
    #state.print_card_state()