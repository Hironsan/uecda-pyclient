# -*- coding: utf-8 -*-
import unittest
from src.cards import Cards
from src.card import Card, Joker, Rank, Suit


class CardStateTest(unittest.TestCase):

    def test_card_num(self):
        cards = []
        state = Cards(cards)
        self.assertEqual(state.card_num(), 0)

        cards = [Card(Rank.Ace, Suit.C)]
        state = Cards(cards)
        self.assertEqual(state.card_num(), 1)

    def test_min_card(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = Cards(cards)
        self.assertEqual(state.min_card(), card1)

        cards = []
        state = Cards(cards)
        self.assertEqual(state.min_card(), [])

    def test_max_card(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = Cards(cards)
        self.assertEqual(state.max_card(), card2)

        cards = []
        state = Cards(cards)
        self.assertEqual(state.max_card(), [])

    def test_suits(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = Cards(cards)
        self.assertEqual(state.suits(), card1.suit + card2.suit)

        card1, card2, card3 = Card(Rank.Three, Suit.D), Card(Rank.Four, Suit.D), Card(Rank.Five, Suit.D)
        cards = [card1, card2, card3]
        state = Cards(cards)
        self.assertEqual(state.suits(), Suit.D)

        cards = []
        state = Cards(cards)
        self.assertEqual(state.suits(), Suit.Null)

    def test_is_pair(self):
        card1, card2 = Card(Rank.Three, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = Cards(cards)
        self.assertFalse(state.is_pair())

        card1, card2 = Card(Rank.Ace, Suit.D), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = Cards(cards)
        self.assertTrue(state.is_pair())

        cards = []
        state = Cards(cards)
        self.assertFalse(state.is_pair())

    def test_is_kaidan(self):
        card1, card2, card3 = Card(Rank.King, Suit.C), Card(Rank.Ace, Suit.C), Card(Rank.Two, Suit.C)
        cards = [card1, card2, card3]
        state = Cards(cards)
        self.assertTrue(state.is_kaidan())

        card1, card2 = Card(Rank.King, Suit.C), Card(Rank.Ace, Suit.C)
        cards = [card1, card2]
        state = Cards(cards)
        self.assertFalse(state.is_kaidan())

        # サーバを信用するか否か
        card1, card2, card3 = Card(Rank.Jack, Suit.C), Card(Rank.Ace, Suit.C), Card(Rank.Two, Suit.C)
        cards = [card1, card2, card3]
        state = Cards(cards)
        self.assertTrue(state.is_kaidan())

        cards = []
        state = Cards(cards)
        self.assertFalse(state.is_pair())

    def test_is_joker_only(self):
        card1, card2 = Joker(Rank.Jack, Suit.X), Card(Rank.Ace, Suit.C)
        cards = [card1]
        state = Cards(cards)
        self.assertTrue(state.is_joker_only())

        cards = [card1, card2]
        state = Cards(cards)
        self.assertFalse(state.is_joker_only())

        cards = []
        state = Cards(cards)
        self.assertFalse(state.is_joker_only())

    def test_is_same_suit(self):
        card1, card2, card3 = Card(Rank.King, Suit.C), Card(Rank.Ace, Suit.C), Card(Rank.Two, Suit.D)
        cards = [card1, card2, card3]
        state = Cards(cards)
        self.assertFalse(state._is_same_suit())

        cards = [card1, card2]
        state = Cards(cards)
        self.assertTrue(state._is_same_suit())

        cards = []
        state = Cards(cards)
        self.assertFalse(state._is_same_suit())

    def test_is_same_rank(self):
        card1, card2, card3 = Card(Rank.King, Suit.C), Card(Rank.King, Suit.D), Card(Rank.Two, Suit.D)
        cards = [card1, card2, card3]
        state = Cards(cards)
        self.assertFalse(state._is_same_rank())

        cards = [card1, card2]
        state = Cards(cards)
        self.assertTrue(state._is_same_rank())

        cards = []
        state = Cards(cards)
        self.assertFalse(state._is_same_rank())

    def test_print(self):
        card1, card2 = Card(Rank.King, Suit.C), Card(Rank.King, Suit.D)
        cards = [card1, card2]
        state = Cards(cards)
        print(state)
