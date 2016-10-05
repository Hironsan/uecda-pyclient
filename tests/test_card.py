# -- coding: utf-8 -*-
import unittest
from src.card import Card, Joker, Rank, Suit


class RankTest(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Rank.Under.name, '0')
        self.assertEqual(Rank.Over.name, '14')
        self.assertEqual(Rank.Three.name, '3')
        self.assertEqual(Rank.King.name, '13')
        self.assertEqual(Rank.Ace.name, '1')
        self.assertEqual(Rank.Two.name, '2')


class CardTest(unittest.TestCase):

    def test_cmp(self):
        d3 = Card(Rank.Three, Suit.D)
        d2 = Card(Rank.Two, Suit.D)
        c2 = Card(Rank.Two, Suit.C)
        joker = Joker(Rank.Ace, Suit.X)
        self.assertTrue(d3 < d2)
        self.assertTrue(d2 > d3)
        self.assertTrue(d2 < c2)
        self.assertTrue(c2 > d2)
        self.assertTrue(d3 < joker)
        self.assertTrue(d2 < joker)
        self.assertTrue(d2 == d2)

    def test_str(self):
        self.assertEqual(str(Card(Rank.Ace, Suit.C)), 'C1')
        self.assertEqual(str(Card(Rank.Ace, Suit.X)), 'X1')
