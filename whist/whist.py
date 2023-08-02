import asyncio
import itertools

values = [str(i) for i in range(2,11)] + ["J","Q","K","A"]
values_verbose = ["two","three","four","five","six","seven","eight","nine","ten","jack","queen","king"]
suits  = ["H","C","D","S"]
suits_verbose = ["hearts","clubs","diamonds","spades"]
suit_symbols = ["♡", "♧" ,"♢", "♤"]
# ♠♥♦♣ 
# ♤♡♢♧ 

# Whether to enable the rule where you aren't allowed to sum to the correct amount
NO_CORRECT_TOTAL = True


def get_symbol(suit):
    return suit_symbols[suits.index(suit)]


class Player:
    def __init__(self):
        # Cards seen played in previous rounds, never includes this player's hand or cards from this round
        self.cards_seen = []
        self.player_no = None
        self.ui = None

    async def bid(self, hand, trump_suit, previous_bids, num_players):
        return 0
    
    async def play(self, hand, trump_suit, previous_cards, bids, tricks):
        return hand[0]
    
    # Allow Players to update which cards have been played at the end of each round
    def cards_played(self, cards):
        for card in cards:
            if card not in self.cards_seen:
                self.cards_seen.append(card)
    
    def clear(self):
        self.cards_seen = []
    
    def __str__(self):
        return "Unknown player"
    

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def get_val(self):
        return values.index(self.value)
    
    def __repr__(self):
        return self.value + get_symbol(self.suit)

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit
    
    @classmethod
    def from_str(self, string):
        suit = string[-1]
        assert suit in suits
        value = string[:-1]
        assert value in values
        return Card(value, suit)

def new_deck():
    return [Card(value, suit) for value, suit in itertools.product(values, suits)]
