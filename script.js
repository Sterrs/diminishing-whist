document.getElementById("dealButton").addEventListener("click", dealRandomCards);

function dealRandomCards() {
  const suits = ["♠️", "♥️", "♦️", "♣️"];
  const values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
  const deck = [];

  // Create a standard deck of 52 cards
  for (const suit of suits) {
    for (const value of values) {
      deck.push({ value, suit });
    }
  }

  const randomHand = [];

  // Randomly select 13 cards for the random hand
  for (let i = 0; i < 13; i++) {
    const randomIndex = Math.floor(Math.random() * deck.length);
    randomHand.push(deck.splice(randomIndex, 1)[0]);
  }

  displayHand(randomHand);
}

function displayHand(hand) {
  const cardContainer = document.getElementById("cardContainer");
  cardContainer.innerHTML = ""; // Clear previous cards

  for (const card of hand) {
    const cardElement = createCardElement(card);
    cardContainer.appendChild(cardElement);
  }
}

function createCardElement(card) {
  const cardElement = document.createElement("div");
  cardElement.classList.add("card");

  const valueElement = document.createElement("div");
  valueElement.textContent = card.value;
  cardElement.appendChild(valueElement);

  const suitElement = document.createElement("div");
  suitElement.textContent = card.suit;
  cardElement.appendChild(suitElement);

  cardElement.addEventListener("click", () => {
    logCardValueAndSuit(card.value, card.suit);
  });

  return cardElement;
}

function logCardValueAndSuit(value, suit) {
  console.log("Clicked card:", value, suit);
}

// Example usage:
// dealRandomCards(); // To display a random hand
// Or, to display a specific hand, call displayHand with the desired collection of cards:
// const myHand = [{ value: "A", suit: "♠️" }, { value: "K", suit: "♦️" }, ... ];
// displayHand(myHand);
