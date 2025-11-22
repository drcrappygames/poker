from .deck import Deck
from .table import Table
from .player import Player
from .evaluator import HandEvaluator


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.table = Table()

    def add_player(self, name, is_human=False):
        self.players.append(Player(name, is_human))

    def reset(self):
        self.deck.reset()
        self.deck.shuffle()
        self.table.reset()
        for p in self.players:
            p.reset_hand()

    def deal_starting_cards(self):
        #rozdaj po 2 karty każdemu z graczy
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.draw())

    def reveal_community_card(self):
        if len(self.table.community_cards) < 5:
            card = self.deck.draw()
            self.table.add_community_card(card)
            return card
        return None

    def evaluate_winner(self):
        best_value = None
        winner = None

        for player in self.players:
            value = HandEvaluator.evaluate(player.hand, self.table.community_cards)

            if best_value is None or value > best_value:
                best_value = value
                winner = player

        return winner, best_value
