class CardRenderer:
    CARD_BACK = "\U0001F0A0"

    SUIT_BASE = {
        "spades":   0x1F0A1,
        "hearts":   0x1F0B1,
        "diamonds": 0x1F0C1,
        "clubs":    0x1F0D1,
    }

    @staticmethod
    def render(card):
        base = CardRenderer.SUIT_BASE[card.suit]
        codepoint = base + (card.rank - 1)
        return chr(codepoint)
