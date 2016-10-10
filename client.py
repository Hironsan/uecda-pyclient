# -*- coding: utf-8 -*-
import enum
from src.connection import Connection
from src.option_parser import OptParser
from src.cards import Cards
from src.strategy import StrategyFactory
from src.hand import Hand
from src.table import Table


class Game(object):
    _continue = 0
    _over = 2

    def __init__(self):
        self._end_flag = self._continue

    def continues(self):
        return self._end_flag == self._continue

    def is_over(self):
        return self._end_flag == self._over

    def set_end_flag(self, flag):
        self._end_flag = flag


def run():
    addr, name, port = OptParser().get_options()  # 引数のチェック.ポート, クライアント名, アドレス
    with Connection(addr, port) as conn:          # サーバーに接続
        conn.send_name(name)                      # サーバーに名前を送信する
        player_id = conn.recv_int()               # プレイヤーidを受け取る
        game = Game()
        while not game.is_over():
            # Before a game
            data = conn.recv_table()                             # 手札を受け取る
            hand = Hand(data)
            table = Table(data)
            if table.is_exchange and table.exchange_num > 0:      # カード交換をする場合は
                factory = StrategyFactory(hand, table)   # カード選択のための戦略クラスを生成する
                strategy = factory.create()
                cards = strategy.select_cards()            # カード交換用のカードを選択する
                data = cards.decode()
                conn.send_table(data)                            # 選択したカードを提出する

            while game.continues():
                # During a game
                data = conn.recv_table()                         # 手札と場の状態を受け取る
                hand = Hand(data)
                table = Table(data)
                if table.is_my_turn:                              # 自分の番だったら
                    factory = StrategyFactory(hand, table)   # カード選択のための戦略クラスを生成する
                    strategy = factory.create()
                    cards = strategy.select_cards()               # カードを選択する
                    data = cards.decode()
                    conn.send_table(data)                        # 選択したカードを提出する
                    was_accepted = conn.recv_int()                # 受理されたかを受け取る

                data = conn.recv_table()                         # 場のカードを受け取る
                field_cards = Hand(data)
                card_state = Cards(field_cards)               # 場のカード状態を決定する

                data = conn.recv_table()  # update field
                end_flag = conn.recv_int()
                game.set_end_flag(end_flag)


if __name__ == '__main__':
    run()
