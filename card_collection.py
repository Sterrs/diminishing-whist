from pyodide.ffi import create_proxy
from pyscript import Element
from js import document
import asyncio

# A file to control the UI elements involved in the hand
HEARTS = "♥️"
CLUBS = "♣️"
DIAMONDS = "♦️"
SPADES = "♠️"

SUITS = ["H", "C", "D", "S"]
SYMBOLS = [HEARTS, CLUBS, DIAMONDS, SPADES]

# Global variable to hold a future which says
fut = None

class CardCollection:
    def __init__(self, container):
        """Given a div, add and remove cards from it, wait for click events etc."""
        self.enabled = False
        self.fut = None
        # Function used to validate card clicks
        # Usually, just to check following suit
        self.validate = None
        self.container = container

    def enable(self):
        """Allow user to click cards"""
        if self.enabled:
            return
        self.enabled = True
        for card in self.container.children:
            card.classList.add("clickable-card")

    def disable(self):
        """Disable user input by clicking cards"""
        if not self.enabled:
            return
        self.enabled = False
        for card in self.container.children:
            card.classList.remove("clickable-card")
     
    async def card_clicked(self, validation=None):
        self.validate = validation
        # Prepare for user click
        self.enable()
        loop = asyncio.get_running_loop()
        self.fut = loop.create_future()
        # Await user click
        value, suit = await self.fut
        # Disallow user click
        self.fut = None
        self.disable()
        return value, suit
    
    def clear(self):
        self.container.innerHTML = ""

    def add_card(self, value, suit):
        element = document.createElement("div")
        element.classList.add("card")
        
        value_element = document.createElement("div")
        value_element.textContent = value
        element.appendChild(value_element)

        suit_element = document.createElement("div")
        if suit == "H" or suit == "D":
            suit_element.style.color = "red"
        suit_element.textContent = SYMBOLS[SUITS.index(suit)]
        element.appendChild(suit_element)

        def on_click(mouse_event):
            if self.fut is not None:
                # Check if this card satisfies the validation conditions
                if self.validate is not None and not self.validate(value, suit):
                    return

                self.fut.set_result((value, suit))
 
                element.style.opacity = 0
                async def wait_then_hide():
                    await asyncio.sleep(0.4)
                    element.style.display = "none"
                asyncio.create_task(wait_then_hide())

        element.addEventListener("click", create_proxy(on_click))

        self.container.appendChild(element)
