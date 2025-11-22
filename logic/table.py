class Table:
    def __init__(self):
        self.community_cards = []

    def reset(self):
        self.community_cards.clear()

    def add_community_card(self, card):
        self.community_cards.append(card)
