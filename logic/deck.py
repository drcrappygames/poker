import random
from .card import Card

class Deck:
    SUITS = ["spades", "hearts", "diamonds", "clubs"]
    RANKS = list(range(1, 14))

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        #świeża talia kart powinna mieć 52 karty, po skończonej grze będzie reset
        self.cards = [Card(rank, suit) for suit in self.SUITS for rank in self.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        #weź kartę z góry
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
