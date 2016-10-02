# -*- coding: utf-8 -*-


class Strategy(object):
    """
    カード提出の戦略を記すクラス
    """
    def __init__(self, hand, field, card_state):
        self.card_state = card_state
        self.field = field
        self.hand = hand

    def select_change_cards(self, exchange_num):
        pairs = self.hand.find_pairs()
        cards = pairs[1][:exchange_num]
        if exchange_num == 1:
            return cards[0]
        else:
            return cards[0][0], cards[1][0]

    def select_cards(self):
        if self.field.is_empty:
            if self.field.is_kakumei:
                return self.lead_under_kakumei()
            else:
                return self.lead()
        else:
            if self.field.is_kakumei:
                return self.follow_under_kakumei()
            else:
                return self.follow()

    def lead(self):
        """
        場が空で革命が起きていないときの戦略
        @return:
        """
        kaidans = self.hand.find_kaidans()
        if len(kaidans) != 0:
            max_card_num = max(kaidans)
            return kaidans[max_card_num][0]

        pairs = self.hand.find_pairs()
        if len(pairs) != 0:
            max_card_num = max(pairs)
            return pairs[max_card_num][0]

        return []

    def lead_under_kakumei(self):
        """
        場が空で革命が起きているときの戦略
        @return:
        """
        kaidans = self.hand.find_kaidans()
        if len(kaidans) != 0:
            max_card_num = max(kaidans)
            return kaidans[max_card_num][-1]

        pairs = self.hand.find_pairs()
        if len(pairs) != 0:
            max_card_num = max(pairs)
            return pairs[max_card_num][-1]

        return []

    def follow(self):
        """
        場にカードがあり革命が起きていないときの戦略
        @return:
        """
        if self.card_state.is_kaidan:
            kaidans = self.hand.find_kaidans()
            if kaidans.get(self.card_state.card_num, None):
                return kaidans[self.card_state.card_num][-1]

        if self.card_state.is_pair:
            pairs = self.hand.find_pairs()
            if pairs.get(self.card_state.card_num, None):
                return pairs[self.card_state.card_num][-1]

        return []

    def follow_under_kakumei(self):
        """
        場にカードがあり革命が起きているときの戦略
        @return:
        """
        if self.card_state.is_kaidan:
            kaidans = self.hand.find_kaidans()
            if kaidans.get(self.card_state.card_num, None):
                return kaidans[self.card_state.card_num][0]

        if self.card_state.is_pair:
            pairs = self.hand.find_pairs()
            if pairs.get(self.card_state.card_num, None):
                return pairs[self.card_state.card_num][0]

        return []
