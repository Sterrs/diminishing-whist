import whist


def print_hand(hand, trump_suit, leading_suit=None):
    for suit in whist.suits:
        if leading_suit is not None:
            print(">" if suit == leading_suit else " ", end="")
        print(f"{whist.get_symbol(suit)}", end="")
        print("*" if suit == trump_suit else " ", end="")
        print(": ", end="")
        values = list(k.value for k in filter(lambda c: c.suit == suit, hand))
        sorted_values = reversed(sorted(values, key=whist.values.index))
        print(" ".join(sorted_values))


class UserPlayer(whist.Player):
    def bid(self, hand, trump_suit, previous_bids, num_players):
        print("Your hand is:")
        print_hand(hand, trump_suit)
        #print("The trump suit is:", trump_suit)
        #print("The bids so far are:", previous_bids)
        # TODO: Force last bid to be legal
        bid = input("Type your bid: ")
        return int(bid)
    
    def play(self, hand, trump_suit, previous_cards, bids, tricks):
        if len(previous_cards) > 0:
            leading_suit = previous_cards[0].suit
        else:
            leading_suit = "N/A"
        print("Your hand is:")
        print_hand(hand, trump_suit, leading_suit)
        #print("The trump suit is:", trump_suit)
        #print("The cards played so far are:", previous_cards)
        print("The current tricks of each player are:", tricks)
        print("The bids each player made are        :", bids)
        # TODO: Force follow suit
        card_input = input("Type which card you'd like to play: ")
        card = whist.Card.from_str(card_input)
        return card

    def __str__(self):
        return "User player"
