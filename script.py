import asyncio
from ui import UserInterface
from js import document, createCardElement
from pyodide.ffi import create_proxy

ui = UserInterface()

# ui.set_scores_row(5, [12,13,14,15,16])
# ui.set_turn(4)
# ui.set_player_names(["Jeff", "John", "Simon", "Garfunkel", "Penn"])
# ui.set_player_tricks(0, 0, "??")

async def main():
    def validate(ans):
        pass
    output = await ui.get_bid(5)
    ui.hand.add_card("K", "D")
    ui.hand.add_card("A", "H")
    ui.hand.add_card("A", "D")
    ui.hand.add_card("A", "C")
    ui.hand.add_card("A", "S")
    ui.hand.add_card("A", "C")
    value, suit = await ui.hand.card_clicked()
    ui.add_text("Nice choice")
    trick = ui.new_trick()
    trick.add_card("7", "D")
    trick.add_card("8", "H")
    await asyncio.sleep(1)
    trick.add_card("8", "H")


asyncio.ensure_future(main())
