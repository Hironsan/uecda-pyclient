# -*- coding: utf-8 -*-
import unittest
from src.table import TableEffect


class FieldEffectTest(unittest.TestCase):

    def test_forward(self):
        table = [[0] * 15 for i in range(8)]

        table[5][5] = 1  # 11back中
        table[5][6] = 1  # 革命中
        field_effect = TableEffect(table)
        self.assertTrue(field_effect.is_forward())

        table[5][5] = 0  # 11back中ではない
        table[5][6] = 0  # 革命中ではない
        field_effect = TableEffect(table)
        self.assertTrue(field_effect.is_forward())

        table[5][5] = 1  # 11back中
        table[5][6] = 0  # 革命中ではない
        field_effect = TableEffect(table)
        self.assertFalse(field_effect.is_forward())

        table[5][5] = 0  # 11back中ではない
        table[5][6] = 1  # 革命中
        field_effect = TableEffect(table)
        self.assertFalse(field_effect.is_forward())

    def test_shibari(self):
        table = [[0] * 15 for i in range(8)]

        table[5][7] = 1  # 縛り発生中
        field_effect = TableEffect(table)
        self.assertTrue(field_effect.is_shibari())

        table[5][7] = 0  # 縛りは発生していない
        field_effect = TableEffect(table)
        self.assertFalse(field_effect.is_shibari())

    def test_print(self):
        table = [[0] * 15 for i in range(8)]
        field_effect = TableEffect(table)
        print(field_effect)
