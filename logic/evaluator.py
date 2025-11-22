from itertools import combinations

class HandEvaluator:

    HAND_RANKS = {
        "high_card": 0,
        "pair": 1,
        "two_pair": 2,
        "three": 3,
        "straight": 4,
        "flush": 5,
        "full_house": 6,
        "four": 7,
    }

    @staticmethod
    def evaluate(player_hand, community_cards):
        all_cards = player_hand + community_cards
        best_hand = None

        if len(all_cards) > 5:
            for combo in combinations(all_cards, 5):
                five_cards = list(combo)
                result = HandEvaluator.evaluate_5cards(five_cards)

                if best_hand is None or result > best_hand:
                    best_hand = result

            return best_hand

        return HandEvaluator.evaluate_5cards(all_cards)

    @staticmethod
    def evaluate_5cards(cards):
        ranks = []
        suits = []
        #As może być słaby albo mocny
        for card in cards:
            rank = 14 if card.rank == 1 else card.rank
            ranks.append(rank)
            suits.append(card.suit)

        ranks.sort(reverse=True)

        #Ile razy każda karta występuje
        rank_counts = {}
        for rank in ranks:
            if rank not in rank_counts:
                rank_counts[rank] = 0
            rank_counts[rank] += 1

        count_values = list(rank_counts.values())
        count_values.sort(reverse=True)

        #Kareta - jak 4 karty są takie same
        if 4 in count_values:
            quad_rank = None
            for rank, count in rank_counts.items():
                if count == 4:
                    quad_rank = rank
                    break

            return (HandEvaluator.HAND_RANKS["four"], quad_rank)

        #Full - jak jest para i trójka
        sorted_counts = sorted(rank_counts.values())
        if sorted_counts == [2, 3]:
            triple_rank = None
            for rank, count in rank_counts.items():
                if count == 3:
                    triple_rank = rank
                    break

            return (HandEvaluator.HAND_RANKS["full_house"], triple_rank)

        #Kolor - jak wszystko z jednego 'suit'
        is_flush = len(set(suits)) == 1 and len(cards) == 5
        if is_flush:
            highest_card = max(ranks)
            return (HandEvaluator.HAND_RANKS["flush"], highest_card)

        #Trójka - jak karta występuje 3 razy
        if 3 in count_values:
            triple_rank = None
            for rank, count in rank_counts.items():
                if count == 3:
                    triple_rank = rank
                    break

            return (HandEvaluator.HAND_RANKS["three"], triple_rank)

        #2 pary - jak w ilości kart występują 2 dwójki
        if count_values.count(2) == 2:
            highest_pair = None

            for rank, count in rank_counts.items():
                if count == 2:
                    if highest_pair is None or rank > highest_pair:
                        highest_pair = rank

            return (HandEvaluator.HAND_RANKS["two_pair"], highest_pair)

        #Para - jak mamy 2 karty takie same
        if 2 in count_values:
            pair_rank = None

            for rank, count in rank_counts.items():
                if count == 2:
                    pair_rank = rank
                    break

            return (HandEvaluator.HAND_RANKS["pair"], pair_rank)

        #Wysoka karta - najgorszy przypadek, weź najlepszą kartę
        highest_card = max(ranks)
        return (HandEvaluator.HAND_RANKS["high_card"], highest_card)
