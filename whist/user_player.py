import asyncio
import whist.whist as whist


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
    async def bid(self, hand, trump_suit, previous_bids, num_players):
        if self.ui is None:
            print("Your hand is:")
            print_hand(hand, trump_suit)
            #print("The trump suit is:", trump_suit)
            #print("The bids so far are:", previous_bids)
            # TODO: Force last bid to be legal
            bid = input("Type your bid: ")
            return int(bid)
        
        self.ui.hand.clear()

        sorted_hand = sorted(hand, key=lambda c: (13 - whist.values.index(c.value)) + 13 * ((whist.suits.index(c.suit) - whist.suits.index(trump_suit)) % 4), reverse=False)

        for card in sorted_hand:
            self.ui.hand.add_card(card.value, card.suit)
            await asyncio.sleep(0.1)

        disallow = None 
        if sum((1 for bid in previous_bids if bid is not None)) == num_players - 1:
            disallow = len(hand) - sum((bid for bid in previous_bids if bid is not None))

        bid = await self.ui.get_bid(len(hand), disallow)
        return bid
    
    async def play(self, hand, trump_suit, previous_cards, bids, tricks):
        if len(previous_cards) > 0:
            leading_suit = previous_cards[0].suit
        else:
            leading_suit = "N/A"
        if self.ui is None:
            print("Your hand is:")
            print_hand(hand, trump_suit, leading_suit)
            #print("The trump suit is:", trump_suit)
            #print("The cards played so far are:", previous_cards)
            print("The current tricks of each player are:", tricks)
            print("The bids each player made are        :", bids)
            # TODO: Force follow suit
            card_input = input("Type which card you'd like to play: ")
            card = whist.Card.from_str(card_input)
        else:
            # Which suit we must play. None if any suit is fine
            suits_allowed = None
            if previous_cards != []:
                lead_suit = previous_cards[0].suit

                filtered = list(filter(lambda c: c.suit == lead_suit, hand))
                if filtered:
                    suits_allowed = lead_suit
            value, suit = await self.ui.hand.card_clicked(lambda value, suit: suits_allowed is None or suit == suits_allowed)
            card = whist.Card(value, suit)
        return card

    def __str__(self):
        return "User player"
