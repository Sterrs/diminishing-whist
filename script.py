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

user = random.randint(0,4)
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

asyncio.ensure_future(play(players, True, ui))
