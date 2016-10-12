# -*- coding: utf-8 -*-
import unittest
from src.player import Player, Players


class PlayersTest(unittest.TestCase):

    def test_print(self):
        table = [[0] * 15 for i in range(8)]
        players = Players(table)
        print(players)


class PlayerTest(unittest.TestCase):

    def test_needs_exchange(self):
        data = [[0] * 15 for i in range(8)]
        data[5][0] = 1  # カード交換中か
        data[5][1] = 1  # カード交換の枚数
        player = Player(data)
        self.assertTrue(player.needs_exchange())

        data[5][1] = 2
        player = Player(data)
        self.assertTrue(player.needs_exchange())

        data[5][1] = 0
        player = Player(data)
        self.assertFalse(player.needs_exchange())

        data[5][0] = 0
        player = Player(data)
        self.assertFalse(player.needs_exchange())

        data[5][1] = 1
        player = Player(data)
        self.assertFalse(player.needs_exchange())

    def test_can_submit(self):
        data = [[0] * 15 for i in range(8)]
        player = Player(data)
        self.assertFalse(player.can_submit())

        data[5][2] = 1
        player = Player(data)
        self.assertTrue(player.can_submit())
