import random
import whist

class RandomPlayer(whist.Player):
    def bid(self, hand, trump_suit, previous_bids, num_players):
        num_cards = len(hand)
        mean = num_cards / num_players
        variance = 0.64 * (num_cards ** 2) / (num_players ** 2)
        rand = random.gauss(mean, variance)
        if rand < 0:
            rand = 0
        bid = round(rand)
        # Deal with case where last player
        if whist.NO_CORRECT_TOTAL:
            number_have_bid = sum((1 for b in previous_bids if b is not None))
            previous_sum = sum((b for b in previous_bids if b is not None))
            if number_have_bid == num_players - 1:
                if bid + previous_sum == num_cards:
                    if rand < bid:
                        bid -= 1
                    else:
                        bid += 1
        return bid
    
    def play(self, hand, trump_suit, previous_cards, bids, tricks):
        if previous_cards == []:
            return random.choice(hand)
        leader = previous_cards[0]
        follow_suit = leader.suit
        filtered = list(filter(lambda c: c.suit == follow_suit, hand))
        if filtered == []:
            return random.choice(hand)
        else:
            return random.choice(filtered)
