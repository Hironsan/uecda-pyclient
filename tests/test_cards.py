# -*- coding: utf-8 -*-
import unittest
from src.cards import TableCards, BaseCardSet, NormalCardSet, JokerCardSet
from src.card import Card, Joker, Rank, Suit


class CardStateTest(unittest.TestCase):

    def test_card_num(self):
        cards = []
        state = TableCards(cards)
        self.assertEqual(state.card_num(), 0)

        cards = [Card(Rank.Ace, Suit.C)]
        state = TableCards(cards)
        self.assertEqual(state.card_num(), 1)

    def test_min_card(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = TableCards(cards)
        self.assertEqual(state.min_card(), card1)

        cards = []
        state = TableCards(cards)
        self.assertEqual(state.min_card(), [])

    def test_max_card(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = TableCards(cards)
        self.assertEqual(state.max_card(), card2)

        cards = []
        state = TableCards(cards)
        self.assertEqual(state.max_card(), [])

    def test_suits(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = TableCards(cards)
        self.assertEqual(state.suits(), card1.suit + card2.suit)

        card1, card2, card3 = Card(Rank.Three, Suit.D), Card(Rank.Four, Suit.D), Card(Rank.Five, Suit.D)
        cards = [card1, card2, card3]
        state = TableCards(cards)
        self.assertEqual(state.suits(), Suit.D)

        cards = []
        state = TableCards(cards)
        self.assertEqual(state.suits(), Suit.Null)

    def test_is_pair(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = TableCards(cards)
        self.assertFalse(state.is_pair())

        card1, card2 = Card(Rank.Ace, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = TableCards(cards)
        self.assertTrue(state.is_pair())

        cards = []
        state = TableCards(cards)
        self.assertFalse(state.is_pair())

    def test_is_kaidan(self):
        card1, card2, card3 = Card(Rank.King, Suit.C), Card(Rank.Ace, Suit.C), Card(Rank.Two, Suit.C)
        cards = [card1, card2, card3]
        state = TableCards(cards)
        self.assertTrue(state.is_kaidan())

        card1, card2 = Card(Rank.King, Suit.C), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = TableCards(cards)
        self.assertFalse(state.is_kaidan())

        # サーバを信用するか否か
        card1, card2, card3 = Card(Rank.Jack, Suit.C), Card(Rank.Ace, Suit.C), Card(Rank.Two, Suit.C)
        cards = [card1, card2, card3]
        state = TableCards(cards)
        self.assertTrue(state.is_kaidan())

        cards = []
        state = TableCards(cards)
        self.assertFalse(state.is_pair())

    def test_is_joker_only(self):
        card1, card2 = Joker(Rank.Jack, Suit.X), Card(Rank.Ace, Suit.C)
        cards = [card1]
        state = TableCards(cards)
        self.assertTrue(state.is_joker_only())

        cards = [card1, card2]
        state = TableCards(cards)
        self.assertFalse(state.is_joker_only())

        cards = []
        state = TableCards(cards)
        self.assertFalse(state.is_joker_only())

    def test_is_same_suit(self):
        card1, card2, card3 = Card(Rank.King, Suit.C), Card(Rank.Ace, Suit.C), Card(Rank.Two, Suit.D)
        cards = [card1, card2, card3]
        state = TableCards(cards)
        self.assertFalse(state._is_same_suit())

        cards = [card1, card2]
        state = TableCards(cards)
        self.assertTrue(state._is_same_suit())

        cards = []
        state = TableCards(cards)
        self.assertFalse(state._is_same_suit())

    def test_is_same_rank(self):
        card1, card2, card3 = Card(Rank.King, Suit.C), Card(Rank.King, Suit.D), Card(Rank.Two, Suit.D)
        cards = [card1, card2, card3]
        state = TableCards(cards)
        self.assertFalse(state._is_same_rank())

        cards = [card1, card2]
        state = TableCards(cards)
        self.assertTrue(state._is_same_rank())

        cards = []
        state = TableCards(cards)
        self.assertFalse(state._is_same_rank())

    def test_print(self):
        card1, card2 = Card(Rank.King, Suit.C), Card(Rank.King, Suit.D)
        cards = [card1, card2]
        state = TableCards(cards)
        print(state)


import pprint
class NormalCardSetTest(unittest.TestCase):

    def test_create_kaidan(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[0][2] = 1
        cards[0][4] = 1
        card_set = NormalCardSet(cards)
        kaidans = card_set.create_kaidan()
        self.assertEqual(kaidans[0][0], 0)
        self.assertEqual(kaidans[0][1], 2)
        self.assertEqual(kaidans[0][2], 1)
        self.assertEqual(kaidans[0][3], 0)
        self.assertEqual(kaidans[0][4], 1)
        self.assertEqual(kaidans[0][5], 0)

    def test_create_group(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[1][1] = 1
        card_set = NormalCardSet(cards)
        groups = card_set.create_group()
        self.assertEqual(groups[0][1], 2)
        self.assertEqual(groups[1][1], 2)
        self.assertEqual(groups[2][1], 0)
        self.assertEqual(groups[3][1], 0)

    def test_find_kaidans(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[0][2] = 1
        cards[0][4] = 1
        card_set = NormalCardSet(cards)
        for num, kaidans in card_set.find_kaidans().items():
            for kaidan in kaidans:
                print(' '.join(str(card) for card in kaidan))

    def test_find_groups(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[1][1] = 1
        cards[3][1] = 1
        card_set = NormalCardSet(cards)
        for num, groups in card_set.find_groups().items():
            for group in groups:
                print(' '.join(str(card) for card in group))


class JokerCardSetTest(unittest.TestCase):

    def test_create_kaidan(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[0][2] = 1
        cards[0][4] = 1
        cards[4][1] = 2
        card_set = JokerCardSet(cards)
        kaidans = card_set.create_kaidan()
        self.assertEqual(kaidans[0][0], 3)
        self.assertEqual(kaidans[0][1], 4)
        self.assertEqual(kaidans[0][2], 3)
        self.assertEqual(kaidans[0][3], 2)
        self.assertEqual(kaidans[0][4], 2)
        self.assertEqual(kaidans[0][5], 1)

    def test_create_group(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[1][1] = 1
        cards[4][1] = 2
        card_set = JokerCardSet(cards)
        groups = card_set.create_group()
        self.assertEqual(groups[0][1], 3)
        self.assertEqual(groups[1][1], 3)
        self.assertEqual(groups[2][1], 0)
        self.assertEqual(groups[3][1], 0)

    def test_find_kaidans(self):
        cards = [[0] * 15 for _ in range(8)]
        cards[0][1] = 1
        cards[0][2] = 1
        cards[0][4] = 1
        cards[4][1] = 2
        card_set = JokerCardSet(cards)
        for num, kaidans in card_set.find_kaidans().items():
            for kaidan in kaidans:
                print(' '.join(str(card) for card in kaidan))

    def test_find_groups(self):
        cards = [[0] * 15 for i in range(8)]
        cards[0][1] = 1
        cards[1][1] = 1
        cards[3][1] = 1
        cards[4][1] = 2
        card_set = JokerCardSet(cards)
        for num, groups in card_set.find_groups().items():
            for group in groups:
                print(' '.join(str(card) for card in group))
