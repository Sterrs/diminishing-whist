import math
import logging
import whist


# Compare card1 and card2, assuming follow suit is card1.
# True means card1 < card2
def compare(trump_suit, card1, card2):
    if card1.suit == card2.suit:
        if whist.values.index(card2.value) > whist.values.index(card1.value):
            return True
        else:
            return False
    elif card2.suit == trump_suit:
        return True
    else:
        return False

# Calculate the chance `card` would win if the trump suit was `trump_suit`
# and the remaining possible cards are `possible_cards`
# previous_cards is cards already played in this round
def chance_of_win(num_players, card, trump_suit, possible_cards, previous_cards=None):
    # Check if we've already lost
    if previous_cards is not None:
        for c in previous_cards:
            if compare(trump_suit, card, c):
                return 0

    if previous_cards is None:
        # We don't know whether we'll be leading
        follow_suit = None
        leader_prob = 1 / num_players
    elif previous_cards == []:
        # We're leading
        leader_prob = 1
        follow_suit = None
    else:
        # We aren't leading
        follow_suit = previous_cards[0].suit
        leader_prob = 0
        # If we aren't following suit or trumping, we've lost
        if card.suit != trump_suit and follow_suit != card.suit:
            return 0

    num_possible = len(possible_cards)
    num_of_each_suit = [0,0,0,0]
    # Work out how many of the cards that could come up we would lose to
    lower = 0
    for c in possible_cards:
        num_of_each_suit[whist.suits.index(c.suit)] += 1
        if not compare(trump_suit, card, c):
            lower += 1  
    
    # Players left to play, excluding ourself
    players_left = num_players - 1 - (0 if previous_cards is None else len(previous_cards))
    # if num_possible < players_left:
    #     print(previous_cards)
    #     print(possible_cards)
    #     print(num_possible, players_left)
    prob_win_if_follow = math.comb(lower, players_left) / math.comb(num_possible, players_left)
    
    # If we know what suit is leading, we can be certain whether this card will follow suit
    if follow_suit is not None:
        # We would already have stopped if we weren't trumping or following suit, so ignore
        prob_follow = 1
    # If we don't know what suit will be leading, two cases, trump or non-trump
    else:
        # We have to multipy what we get by the probability that we're actually following suit
        if card.suit == trump_suit:
            prob_follow = 1
        else:
            # If we're not leading, what's the probability of the leader being the same suit?
            prob_leader_suited = num_of_each_suit[whist.suits.index(card.suit)] / num_possible
            prob_follow = leader_prob + (1 - leader_prob) * prob_leader_suited


    return prob_win_if_follow * prob_follow


class ExpectationPlayer(whist.Player): 
    def seen(self, card):
        for c in self.cards_seen:
            if c == card:
                return True
        return False

    def bid(self, hand, trump_suit, previous_bids, num_players):
        num_cards = len(hand)
        cards_left = list(filter(lambda c: c not in hand, whist.new_deck()))
        chances = list((chance_of_win(num_players, c, trump_suit, cards_left) for c in hand))
        estimate = sum(chances)
        # for hand_card, chance in zip(hand, chances):
        #     logging.debug(str(hand_card) + " " + str(chance))
        # logging.debug(str(hand) + " " + str(estimate))
        bid = round(estimate)
        # Deal with being last player
        if whist.NO_CORRECT_TOTAL:
            number_have_bid = sum((1 for b in previous_bids if b is not None))
            previous_sum = sum((b for b in previous_bids if b is not None))
            if number_have_bid == num_players - 1:
                if bid + previous_sum == num_cards:
                    if estimate < bid:
                        bid -= 1
                    else:
                        bid += 1
        return bid
    
    def play(self, hand, trump_suit, previous_cards, bids, tricks):
        num_players = len(bids)
        cards_seen = hand + previous_cards + self.cards_seen
        cards_left = list(filter(lambda c: c not in cards_seen, whist.new_deck()))
        best_card = None
        best_diff = math.inf
        # For each card in our hand, let's see what happens if we play it
        legal_plays = []
        if previous_cards == []:
            legal_plays = hand
        else:
            follow_suit = previous_cards[0].suit
            legal_plays = list(filter(lambda c: c.suit == follow_suit, hand))
            if legal_plays == []:
                legal_plays = hand
        for card in legal_plays:
            # print(str(card) + ": ", end="")
            # First work out the probability of winning with that card
            win_prob = chance_of_win(num_players, card, trump_suit, cards_left, previous_cards)
            # print(f"Prob. of winning round: {win_prob}. ", end="")
            # Now work out the value of the whole hand in that case
            value = 0
            for j, c in enumerate(hand):
                if hand[j] == card:
                    continue
                value += chance_of_win(num_players, c, trump_suit, cards_left)
            # print(f"Value of rest of hand: {value}. ", end="") 
            value += tricks[self.player_no]
            value += win_prob
            # print(f"Total value: {value}")
            # Calculate how far away our expected value is from the bid we made
            diff = abs(value - bids[self.player_no])
            if diff < best_diff:
                best_diff = diff
                best_card = card
 
        return best_card
    