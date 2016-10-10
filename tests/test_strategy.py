# -*- coding: utf-8 -*-
import unittest
from src.table import TableEffect
from src.hand import Hand
from src.cards import Cards
from src.strategy import StrategyFactory, ExchangeStrategy, ForwardStrategy, ReverseStrategy


class StrategyFactoryTest(unittest.TestCase):

    def setUp(self):
        """
        場の状態を用意しておく。
        いまのところ以下の2つ
        * 革命状態
        * 非革命状態
        """
        self.hand = Hand()
        self.card_state = Cards()
        self.field_effect = TableEffect()

    def test_create(self):
        pass


class ExchangeStrategyTest(unittest.TestCase):

    def setUp(self):
        """
        様々な手札を用意しておく。
        """
        self.hand = Hand()
        self.card_state = Cards()
        self.field_effect = TableEffect()

    def test_select_cards(self):
        pass


class ForwardStrategyTest(unittest.TestCase):

    def setUp(self):
        """
        様々な手札、場の状態を用意しておく。
        """
        self.hand = Hand()
        self.card_state = Cards()
        self.field_effect = TableEffect()

    def test_select_cards(self):
        pass


class ReverseStrategyTest(unittest.TestCase):

    def setUp(self):
        """
        様々な手札、場の状態を用意しておく。
        """
        self.hand = Hand()
        self.card_state = Cards()
        self.field_effect = TableEffect()

    def test_select_cards(self):
        pass
