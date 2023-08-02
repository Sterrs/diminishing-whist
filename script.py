import asyncio
import random
from whist.play import play
from whist.expectation_player import ExpectationPlayer
from whist.user_player import UserPlayer
from ui import UserInterface

ui = UserInterface()

opponent_names = [
    "James",
    "Daniel",
    "Michael",
    "David",
    "Henry",
    "Jack",
    "Joseph",
    "Robert",
    "Samuel",
    "Mary",
    "Sarah",
    "Richard",
    "Elizabeth",
    "Oliver",
    "Alexander",
    "Anna",
    "Martin",
    "Olivia",
    "Noah",
    "Benjamin",
    "Emma",
    "Peter",
    "Anthony",
    "Edward",
    "Jason",
    "Joe",
    "Thomas",
    "Sophie",
    "Will",
    "Jane",
    "William",
    "Anna",
    "Stephanie",
    "Ella",
    "Callum",
    "John",
]

user = 4#random.randint(0,4)
players = []
names = []
for i in range(5):
    if i == user:
        players.append(UserPlayer())
        names.append("You")
    else:
        players.append(ExpectationPlayer())
        name = random.choice(opponent_names)
        names.append(random.choice(opponent_names))
        opponent_names.remove(name)
        
ui.set_player_names(names)

async def main():
    scores = await play(players, True, ui)
    place = sorted(scores, reverse=True).index(scores[user])
    suffixes = ["won!", "came second.", "came third.", "came fourth.", "came last."]
    text = f"You {suffixes[place]} Your score was {scores[user]}."
    ui.add_subheading(text)


asyncio.ensure_future(main())
