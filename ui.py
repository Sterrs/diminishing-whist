import asyncio
from card_collection import CardCollection
from pyscript import Element
from pyodide.ffi import create_proxy
from js import document
# This file will manage the HTML DOM through the UserInterface class
# This file does not care about any logic or anything so it's just a bunch of getters and setters


player_letters = "ABCDE"
class UserInterface:
    """Just a wrapper class to avoid having to actually deal with the DOM"""
    def __init__(self):
        self.scores_table = Element("scoresTable")
        self.player_boxes = Element("playerBoxes")
        self.hand_container = Element("handContainer")
        self.hand = CardCollection(self.hand_container.element)
        self.main_content_area = Element("mainContentArea")
        self.current_turn = None

    def set_scores_row(self, row_number, scores):
        table_body = self.scores_table.element.children[1]
        row = table_body.children[row_number]
        for i, cell in enumerate(row.children):
            if i == 0:
                continue
            cell.innerText = scores[i-1]
    
    def set_player_names(self, player_names):
        for i, player_box in enumerate(self.player_boxes.element.children):
            player_box.children[0].innerText = f"Player {player_letters[i]}: {player_names[i]}"

    def set_player_tricks(self, player_number, tricks_obtained, tricks_bid):
        player_box = self.player_boxes.element.children[player_number]
        player_box.children[1].innerText = f"Tricks: {tricks_obtained}/{tricks_bid}"

    def set_turn(self, player_number):
        if player_number is not None:
            player_box = self.player_boxes.element.children[player_number]
            player_box.classList.add("current-player-box")
        if self.current_turn is not None:
            current_turn_player_box = self.player_boxes.element.children[self.current_turn]
            current_turn_player_box.classList.remove("current-player-box")
        self.current_turn = player_number
    
    def clear_main_content(self):
        self.main_content_area.element.innerHTML = ""
    
    async def get_bid(self, max, disallow=None):
        """Provide a text box for the user to fill, and hide it upon submission."""
        input_element = document.createElement("input")
        input_element.setAttribute("type", "number")
        input_element.setAttribute("placeholder", "0")
        input_element.setAttribute("min", 0)
        input_element.setAttribute("max", max)

        loop = asyncio.get_running_loop()
        fut = loop.create_future()

        def validate(event):
            val = input_element.value
            try:
                int_val = int(val)
            except ValueError:
                return False
            
            if int_val < 0 or int_val > max:
                return False
            
            if int_val == disallow:
                return False
            return True

        def on_input(val):
            if not validate(val):
                input_element.classList.add("invalid")
            else:
                input_element.classList.remove("invalid")

        input_element.addEventListener("input", create_proxy(on_input))

        def submit(event):
            val = input_element.value
            
            if event.keyCode != 13 or not validate(val):
                return 
             
            fut.set_result(val)
            self.main_content_area.element.removeChild(input_element)
 
        input_element.addEventListener("keydown", create_proxy(submit))

        self.main_content_area.element.append(input_element)

        output = await fut
        return output


    def new_trick(self):
        """Create a new trick and return the corresponding CardCollection"""
        element = document.createElement("div")
        element.classList.add("card-container")
        self.main_content_area.element.append(element)
        return CardCollection(element)

    def add_text(self, text):
        element = document.createElement("p")
        element.innerText = text
        self.main_content_area.element.append(element)
