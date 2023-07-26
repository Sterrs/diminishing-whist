from js import displayHand

#print("Hello World!")
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
ace_spades = Card("A", "️♠️")
king_diamonds = Card("K", "️♥️")
displayHand([ace_spades, king_diamonds])

def log_card_value_and_suit(value, suit):
    print(value, suit)
