# -*- coding: utf-8 -*-
import sys
from .connection import Connection
from .option_parser import OptParser
from .card_state import CardState
from .strategy import Strategy
from .codec import Decoder, Encoder
from .hand import Hand
from .field import Field


class Client(object):
    """
    ゲーム全体の流れをコントロールするクラス
    """
    def __init__(self):
        addr, name, port = OptParser().get_options()  # 引数のチェック.ポート, クライアント名, アドレス
        self.conn = Connection(addr, port)            # サーバーに接続
        self.conn.send_name(name=name)                # サーバーに名前を送信する
        self.player_id = self.conn.recv_int()         # プレイヤーidを受け取る

    def run(self):
        while True:
            table = self.conn.recv_table()                                # 手札を受け取る
            hand = Hand(Decoder().to_cards(table))
            print(hand)
            field = Field(table)
            if field.is_exchange and field.exchange_num > 0:              # カード交換をする場合は
                strategy = Strategy(hand, field, CardState([]))           # カード選択のための戦略クラスを生成する
                cards = strategy.select_change_cards(field.exchange_num)  # カード交換用のカードを選択する
                table = Encoder().to_table(cards)
                self.conn.send_table(table)                               # 選択したカードを提出する
            self.start_one_game()                                         # 1ゲームを始める

    def start_one_game(self):
        card_state = CardState([])
        while True:
            table = self.conn.recv_table()                    # 手札と場の状態を受け取る
            hand = Hand(Decoder().to_cards(table))
            print("hand", hand)
            field = Field(table)
            print("my_turn", field.is_my_turn)
            if field.is_my_turn:                              # 自分の番だったら
                strategy = Strategy(hand, field, card_state)  # カード選択のための戦略クラスを生成する
                cards = strategy.select_cards()               # カードを選択する
                print(" ".join(str(card) for card in cards))
                table = Encoder().to_table(cards)
                self.conn.send_table(table)                   # 選択したカードを提出する
                was_accepted = self.conn.recv_int()           # 受理されたかを受け取る
                print("accept =", was_accepted)

            table = self.conn.recv_table()                    # 場のカードを受け取る
            field_cards = Hand(Decoder().to_cards(table))
            print("field", " ".join(str(card) for card in field_cards))
            card_state = CardState(field_cards)               # 場のカード状態を決定する

            is_end = self.conn.recv_int()  # ゲームが終わったかを受け取る
            print("end", is_end)
            if is_end == 1:                # 1ゲーム終了のとき
                return                     # self.runに戻る
            elif is_end == 2:              # 全ゲーム終了のとき
                self.conn.close()          # 接続を閉じてから
                sys.exit(0)                # プログラムを終了する

if __name__ == '__main__':
    client = Client()
    client.run()