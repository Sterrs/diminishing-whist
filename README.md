# Diminishing Whist

## Rules

### Introduction

Diminshing Whist is a trick-taking card game for four or five players which is played with a standard deck of 52 playing cards.
The game is split into ten rounds, each of which either has or does not have a trump suit associated with it, as well as a number of cards
dealt in that round. For example, the first round 10♥️ has trump suit hearts and ten cards are dealt to each player. 6**NT on the other hand has
no trump suit and six cards are dealt.
At the beginning of each round, the specified number of cards are dealt to each player. The round is split into two phases, a bidding phase and a
trick-taking phase.

### Bidding

Each player looks at their hand and makes a bid, i.e. makes a prediction of how many 'tricks' they will win. 10 additional points are awarded to
those who obtain exactly as many tricks as they bid at the start of the round, in addition to awarding one point for each trick obtained to every player.
However, if you obtain *more* tricks than you bid, you get zero for that round.

Additionally, the last player is not permitted to bid the number of tricks which would make the total sum of all players' bids be exactly the number
of tricks available.

Players take it in turns to bid first in each round, with this role proceeding clockwise around the table.

### Trick-taking

The trick-taking phase of each round consists of a number of tricks. In each trick, every player must play exactly one card. Thus the number
of tricks available in each round is exactly as many as the number of cards dealt to each player. Each trick has a leader, who is the person who 
won the previous trick, except in the first trick of each round, where it is the person who bid first.

Whoever leads decides what the suit for that round is, by playing a card of that suit. All other players *must* play a card of that suit if they have
one in their hand. If they do not, they may play a card from any suit of their choosing.

The player who plays the highest trump card wins the round. If no trump card is played, the player who plays the highest card of the suit which
was played by the leader wins the round. Within suits, cards are ordered with Ace being the highest and Two being the lowest.

### Winning

The player with the highest score wins. Getting a high score depends on whether your bids are wise and whether your play suits the
cards you have and the bid you made. This eliminates some of the luck from the game.

## About

This is a very rushed website I threw together to allow people to play against my (terrible) Diminishing Whist engines.
Hopefully in the future I can make some which are vaguely competent at the game.

For those that are interested, here's a vague overview of the project. The site is written in pure HTML with CSS.
Most of the code is written in Python and runs locally via PyScript. PyScript is just CPython but compiled to WASM and
running in the browser. This explains the slow-ish loading time of the page. If anything breaks, it's almost certainly
because the PyScript stuff that gets fetched when the page loads has changed.

ChatGPT was immensely helpful in designing the interface and generally providing lots of the HTML and CSS code. Most
weird quirks are a product of that and me just changing random things until it looks right.

The AIs themselves are extremely simple. For bidding, they try to estimate the expected value of their hand by
working out the probability of each of their cards winning a random round from the remaining cards (the cards from that
round being chosen at random, one improvement would be to take into account the fact that players must follow suit).
They then bid whatever is closest to the sum of those probabilities.

For playing cards, they play whichever card makes their expected number of tricks closest to the number of tricks they
bid in the same manner.

You don't need me to explain all the flaws with this approach, just try playing against them. See how high of a score
you can get.

In the future I might try to apply some machine learning techniques to make some stronger players.

