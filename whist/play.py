import asyncio
import logging
import random
import whist.whist as whist
from whist.random_player import RandomPlayer
from whist.user_player import UserPlayer
from whist.expectation_player import ExpectationPlayer

WAIT = 0.75
LETTERS = "ABCDE"

def deal(num_players, num_cards):
    deck = whist.new_deck()
    random.shuffle(deck)
    return [deck[num_cards*i:num_cards*(i+1)] for i in range(num_players)]


# cards_played must be in correct order
# This code works fine if there is no trump suit, of course
def winner(trump_suit, cards_played):
    leader = cards_played[0]
    follow_suit = leader.suit
    card_vals = []
    for card in cards_played:
        val = card.get_val()
        if card.suit == trump_suit:
            val += 14
        elif card.suit == follow_suit:
            val += 1
        else:
            val = 0
        card_vals.append(val)
    return card_vals.index(max(card_vals))


async def bidding(players, hands, starting_player, trump_suit, sleep=False, ui=None):
    num_players = len(players)
    num_cards = len(hands[0])
    bids = [None] * num_players
    for j in range(starting_player, starting_player + num_players):
        if ui is not None:
            ui.set_turn(j % num_players)
        player = players[j % num_players]
        bid = await player.bid(hands[j % num_players], trump_suit, bids, num_players)
        logging.debug(f"Player {(j % num_players) + 1} bids {bid}.")
        if ui is not None:
            ui.add_text(f"Player {LETTERS[j % num_players]} bids {bid}.")
            ui.set_player_tricks(j % num_players, 0, bid)
        if sleep:
            await asyncio.sleep(0.5*WAIT)
        bids[j % num_players] = bid
    # Can't all make bids
    if whist.NO_CORRECT_TOTAL:
        assert sum(bids) != num_cards
    logging.info(f"Bids for this round are {bids}")
    if sleep:
        await asyncio.sleep(3*WAIT)
    return bids


async def trick(players, hands, bids, tricks, starting_player, trump_suit, sleep=False, ui=None):
    if ui is not None:
        trick_container = ui.new_trick()
    num_players = len(players)
    num_cards = len(hands[0])
    cards_played = []
    for j in range(starting_player, starting_player + num_players):
        if ui is not None:
            ui.set_turn(j % num_players)
        player = players[j % num_players]
        hand = hands[j % num_players]
        card = await player.play(hand, trump_suit, cards_played, bids, tricks)

        if ui is not None:
            trick_container.add_card(card.value, card.suit)
        card_str = str(card)
        if len(card_str) == 2:
            card_str = " " + card_str
        if card.suit == trump_suit:
            card_str += "*"
        logging.debug(f"Player {(j % num_players) + 1} played {card_str}")
        if sleep:
            await asyncio.sleep(0.5*WAIT)

        assert card in hand
        if cards_played != []:
            leader = cards_played[0]
            assert leader.suit == card.suit or not any((card.suit == leader.suit for card in hand))
        cards_played.append(card)
        hand.remove(card)
    # Tell each player which cards were played this round
    for player in players:
        player.cards_played(cards_played)
    return (winner(trump_suit, cards_played) + starting_player) % num_players


# Players are pairs (bidding, play) where
# If ui is not None, assume we are just running in the terminal
async def play(players, sleep=False, ui=None):
    for i, player in enumerate(players):
        player.player_no = i
        player.ui = ui

    num_players = len(players)
    suit_rounds = whist.suits + ["NT"]
    scores = [0] * num_players
    logging.debug(f"Playing with {num_players} players: ", *(str(player) for player in players))
    # For each of the ten rounds:
    for i, num_cards in enumerate(range(10, 0, -1)):
        # Forget which cards we've seen
        for j, player in enumerate(players):
            player.clear()
            ui.set_player_tricks(j, 0, "??")
        # Deal
        logging.info(f"Round {num_cards}:")
        hands = deal(num_players, num_cards)
        # Calculate which player starts and trump suit
        starting_player = i % num_players
        trump_suit = suit_rounds[i % 5]
        if ui is not None:
            ui.add_round(num_cards, trump_suit)
        logging.info(f"Trump suit is {whist.get_symbol(trump_suit) if trump_suit != 'NT' else 'No Trump'}")
        # Bid
        logging.debug(f"Cards dealt. Commence bidding:")
        
        bids = await bidding(players, hands, starting_player, trump_suit, sleep, ui)
 
        # Play
        tricks = [0] * num_players
        for trick_num in range(1,num_cards+1):
            if ui is not None:
                ui.add_subheading(f"Trick {trick_num}")
            logging.debug(f"Trick {trick_num} out of {num_cards}.")
            logging.debug(f"Tricks won for this round so far are: {tricks}")

            trick_winner = await trick(players, hands, bids, tricks, starting_player, trump_suit, sleep, ui)

            logging.debug(f"Player {trick_winner + 1} won the trick.")
            if ui is not None:
                ui.add_text(f"Player {LETTERS[trick_winner]} wins the trick.")
                ui.set_player_tricks(trick_winner, tricks[trick_winner] + 1, bids[trick_winner])
            if sleep:
                await asyncio.sleep(3*WAIT)
            tricks[trick_winner] += 1
            starting_player = trick_winner
        logging.info(f"Tricks won: {tricks}")
        
        scores_this_round = []
        for j, (bid, tricks_won) in enumerate(zip(bids, tricks)):
            score = 0
            if bid == tricks_won:
                score += 10
            if tricks_won <= bid:
                score += tricks_won
            logging.debug(f"Player {j+1} scored {score} in this round")
            scores[j] += score
            scores_this_round.append(tricks_won)
        if ui is not None:
            ui.set_scores_row(i, scores)
        logging.info(f"The current scores are {scores}")
        if sleep:
            await asyncio.sleep(5*WAIT)
        if ui is not None:
            ui.clear_main_content()
    return scores
    

if __name__ == "__main__":
    num_players = 5
    sleep = False
    if sleep:
        logging_level = logging.DEBUG
    else:
        # logging_level = logging.INFO
        logging_level = logging.WARNING
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging_level)
    N = 100
    # play([RandomPlayer() for _ in range(5)], sleep=False)
    total_rand = 0
    max_total_rand = 0
    for i in range(N):
        scores = play([RandomPlayer() for _ in range(num_players)], sleep=sleep)
        max_total_rand += max(scores)
        total_rand += sum(scores)
    total_exp = 0
    max_total_exp = 0
    for i in range(N):
        scores = play([ExpectationPlayer() for _ in range(num_players)], sleep=sleep)
        max_total_exp += max(scores)
        total_exp += sum(scores)
    print(f"Random: {total_rand / (100 * num_players)}, {max_total_rand / 100}")
    print(f"Expectation: {total_exp / (100 * num_players)}, {max_total_exp / 100}")


# TODO:
# User input validation (crashes are sad)
