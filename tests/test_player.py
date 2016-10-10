# -*- coding: utf-8 -*-
import unittest
from src.player import Players


class PlayersTest(unittest.TestCase):

    def test_print(self):
        table = [[0] * 15 for i in range(8)]
        players = Players(table)
        print(players)
