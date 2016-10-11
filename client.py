# -*- coding: utf-8 -*-
import enum
from src.connection import Connection
from src.option_parser import OptParser
from src.cards import TableCards
from src.strategy import StrategyFactory
from src.hand import Hand
from src.table import TableEffect
from src.player import Players, Player


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


class Client(object):

    def __init__(self):
        addr, name, port = OptParser().get_options()  # 引数のチェック.ポート, クライアント名, アドレス
        self._addr = addr
        self._port = port
        self._name = name

    def run(self):
        with Connection(self._addr, self._port) as conn:          # サーバーに接続
            conn.send_name(self._name)                      # サーバーに名前を送信する
            player_id = conn.recv_int()               # プレイヤーidを受け取る
            game = Game()
            while not game.is_over():
                game = Game()
                # Before a game
                data = conn.recv_table()                             # 手札を受け取る
                hand = Hand(data)
                table = TableEffect(data)
                player = Player(data)
                if player.needs_exchange():      # カード交換をする場合は
                    factory = StrategyFactory(hand, table)   # カード選択のための戦略クラスを生成する
                    strategy = factory.create()
                    cards = strategy.select_cards()            # カード交換用のカードを選択する
                    #data = cards.decode()
                    data = [[0] * 15 for i in range(8)]
                    conn.send_table(data)                            # 選択したカードを提出する

                while game.continues():
                    # During a game
                    data = conn.recv_table()                         # 手札と場の状態を受け取る
                    hand = Hand(data)
                    table = TableEffect(data)
                    player = Player(data)
                    if player.can_submit():                              # 自分の番だったら
                        factory = StrategyFactory(hand, table)   # カード選択のための戦略クラスを生成する
                        strategy = factory.create()
                        cards = strategy.select_cards()               # カードを選択する
                        #data = cards.decode()
                        data = [[0] * 15 for i in range(8)]
                        conn.send_table(data)                        # 選択したカードを提出する
                        was_accepted = conn.recv_int()                # 受理されたかを受け取る

                    data = conn.recv_table()                         # 場のカードを受け取る
                    table_cards = TableCards(data)               # 場のカード状態を決定する

                    end_flag = conn.recv_int()
                    game.set_end_flag(end_flag)


if __name__ == '__main__':
    client = Client()
    client.run()
