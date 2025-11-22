class Card:
    def __init__(self, rank: int, suit: str):

        #rank: 1–13  1 lub 14=As, 11=walet, 12=królowa, 13=król
        self.rank = rank
        #suit: spades, hearts, diamonds, clubs
        self.suit = suit
