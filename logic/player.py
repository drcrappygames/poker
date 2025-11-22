class Player:
    def __init__(self, name: str, is_human: bool = False):
        self.name = name
        self.is_human = is_human
        self.hand = []

    def reset_hand(self):
        self.hand.clear()

    def receive_card(self, card):
        self.hand.append(card)
