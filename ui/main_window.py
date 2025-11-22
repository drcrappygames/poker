import tkinter as tk
from logic.game import Game
from .card_renderer import CardRenderer


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Poker")

        self.game = Game()
        self.game.add_player("Gracz 1", is_human=True)  # bottom
        self.game.add_player("Gracz 2")  # left
        self.game.add_player("Gracz 3")  # top
        self.game.add_player("Gracz 4")  # right

        # zielony stół
        self.canvas = tk.Canvas(
            root, width=500, height=500,
            bg="#1A472A"
        )
        self.canvas.pack()

        self.winner_text_id = None

        # Nazwy graczy
        self.player_labels = {
            'top':    self.canvas.create_text(250,  30, text="Gracz 3", fill="white", font=("Arial", 14)),
            'bottom': self.canvas.create_text(250, 495, text="Gracz 1", fill="white", font=("Arial", 14)),
            'left':   self.canvas.create_text( 50, 300, text="Gracz 2", fill="white", font=("Arial", 14)),
            'right':  self.canvas.create_text(450, 300, text="Gracz 4", fill="white", font=("Arial", 14)),
        }

        # Widoki kart
        self.card_labels = {
            'top':    self.canvas.create_text(250,  70, text="", fill="white", font=("Arial", 56)),
            'bottom': self.canvas.create_text(250, 420, text="", fill="white", font=("Arial", 72)),
            'left':   self.canvas.create_text(60, 250, text="", fill="white", font=("Arial", 56)),
            'right':  self.canvas.create_text(440, 250, text="", fill="white", font=("Arial", 56)),
        }

        # Karty wspólne
        self.community_labels = [
            self.canvas.create_text(150, 250, text="", fill="white", font=("Arial", 64)),
            self.canvas.create_text(200, 250, text="", fill="white", font=("Arial", 64)),
            self.canvas.create_text(250, 250, text="", fill="white", font=("Arial", 64)),
            self.canvas.create_text(300, 250, text="", fill="white", font=("Arial", 64)),
            self.canvas.create_text(350, 250, text="", fill="white", font=("Arial", 64)),
        ]

        # przyciski
        self.btn_draw = tk.Button(root, text="Dobierz", command=self.on_draw)
        self.btn_check = tk.Button(root, text="Sprawdź", command=self.on_check)
        self.btn_reset = tk.Button(root, text="Reset", command=self.on_reset)
        self.btn_draw.pack(pady=5)
        self.btn_check.pack(pady=5)
        self.btn_reset.pack(pady=5)
        self.btn_reset.pack_forget()

        self.start_new_game()

    def start_new_game(self):
        if self.winner_text_id:
            self.canvas.delete(self.winner_text_id)
            self.winner_text_id = None

        self.game.reset()
        self.game.deal_starting_cards()
        self.update_ui()

    def update_ui(self):
        self.render_player_cards()

        #Pokaz karty wspólne
        community = self.game.table.community_cards
        for i, card_label in enumerate(self.community_labels):
            if i < len(community):
                symbol = CardRenderer.render(community[i])
            else:
                symbol = ""
            self.canvas.itemconfig(card_label, text=symbol)

    #renderuj tylko karty gracza, pozostałe zostają ukrtye
    def render_player_cards(self):
        CARD_BACK = CardRenderer.CARD_BACK

        #karty gracza pokaż od razu
        human = self.game.players[0]
        human_symbols = "".join(CardRenderer.render(c) for c in human.hand)
        self.canvas.itemconfig(self.card_labels['bottom'], text=human_symbols)

        #karty npc'tów pokaż odwrócone
        for index, pos in zip([1, 2, 3], ['left', 'top', 'right']):
            npc = self.game.players[index]
            cards_text = "".join(CARD_BACK for _ in npc.hand)
            self.canvas.itemconfig(self.card_labels[pos], text=cards_text)

    def on_draw(self):
        card = self.game.reveal_community_card()
        if card is None:
            self.on_check()
        else:
            self.update_ui()

    def on_check(self):
        winner, value = self.game.evaluate_winner()

        self.reveal_all_cards()
        self.show_winner_on_canvas(winner.name, value)

        self.btn_draw.pack_forget()
        self.btn_check.pack_forget()
        self.btn_reset.pack(pady=5)

    def on_reset(self):
        self.btn_reset.pack_forget()

        self.btn_draw.pack(pady=5)
        self.btn_check.pack(pady=5)

        self.start_new_game()

    #renderuj karty wszystkich graczy jako odpowiadające im kody unicode
    def reveal_all_cards(self):
        for i, pos in zip([0, 1, 2, 3], ['bottom', 'left', 'top', 'right']):
            player = self.game.players[i]
            symbols = "".join(CardRenderer.render(c) for c in player.hand)
            self.canvas.itemconfig(self.card_labels[pos], text=symbols)

    def show_winner_on_canvas(self, name, value):

        display_ranks = {
            0: "Wysoką kartą",
            1: "Parą",
            2: "Dwiema parami",
            3: "Trójką",
            4: "Straight",
            5: "Kolorem",
            6: "Karetą"
        }

        text = f"Wygrał: {name} z {display_ranks[value[0]]}"

        self.winner_text_id = self.canvas.create_text(
            250, 180,
            text=text,
            fill="yellow",
            font=("Arial", 18, "bold")
        )