# -*- coding: utf-8 -*-
import enum
from .connection import Connection
from .option_parser import OptParser
from .card_state import CardState
from .strategy import Strategy
from .hand import Hand
from .field import Field


class Game(enum.Enum):
    cont = 0
    comp = 1
    over = 2


def update_field(conn):
    end_flag = conn.recv_int()
    return Game(end_flag)


def update_end_flag(conn):
    end_flag = conn.recv_int()
    return Game(end_flag)


def run():
    addr, name, port = OptParser().get_options()  # 引数のチェック.ポート, クライアント名, アドレス
    with Connection(addr, port) as conn:          # サーバーに接続
        conn.send_name(name)                      # サーバーに名前を送信する
        player_id = conn.recv_int()               # プレイヤーidを受け取る
        end_flag = Game.cont
        while end_flag is not Game.over:
            # Before a game
            table = conn.recv_table()                             # 手札を受け取る
            hand = Hand(table)
            field = Field(table)
            if field.is_exchange and field.exchange_num > 0:      # カード交換をする場合は
                strategy = Strategy(hand, field, CardState([]))   # カード選択のための戦略クラスを生成する
                cards = strategy.select_change_cards()            # カード交換用のカードを選択する
                table = cards.decode()
                conn.send_table(table)                            # 選択したカードを提出する
            card_state = CardState([])
            while end_flag is Game.cont:
                # During a game
                table = conn.recv_table()                         # 手札と場の状態を受け取る
                hand = Hand(table)
                field = Field(table)
                if field.is_my_turn:                              # 自分の番だったら
                    strategy = Strategy(hand, field, card_state)  # カード選択のための戦略クラスを生成する
                    cards = strategy.select_cards()               # カードを選択する
                    table = cards.decode()
                    conn.send_table(table)                        # 選択したカードを提出する
                    was_accepted = conn.recv_int()                # 受理されたかを受け取る

                table = conn.recv_table()                         # 場のカードを受け取る
                field_cards = Hand(table)
                card_state = CardState(field_cards)               # 場のカード状態を決定する

                update_field(conn)
                end_flag = update_end_flag(conn)


if __name__ == '__main__':
    run()
