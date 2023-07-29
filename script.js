// Get the menu icon and menu elements
const menuIcon = document.querySelector('.menu-icon');
const menu = document.querySelector('.menu');

// Add a click event listener to the menu icon to toggle the menu
menuIcon.addEventListener('click', () => {
    menu.classList.toggle('menu-open');
});

// Hide the menu when clicking outside of it
document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && !menuIcon.contains(event.target)) {
        menu.classList.remove('menu-open');
    }
});

// function displayHand(hand) {
//   const cardContainer = document.getElementById("cardContainer");
//   cardContainer.innerHTML = ""; // Clear previous cards
// 
//   for (const card of hand) {
//     const cardElement = createCardElement(card);
//     cardContainer.appendChild(cardElement);
//   }
// }

// TODO: Move to Python
function createCardElement(card, clickHandler=null) {
  const cardElement = document.createElement("div");
  if (clickHandler) {
    cardElement.classList.add("clickable-card")
  }
  cardElement.classList.add("card");

  const valueElement = document.createElement("div");
  valueElement.textContent = card.value;
  cardElement.appendChild(valueElement);

  const suitElement = document.createElement("div");
  suitElement.textContent = card.suit;
  cardElement.appendChild(suitElement);
  if (clickHandler) {
    cardElement.addEventListener("click", () => {
      var clear_card = clickHandler(card.value, card.suit);
      if (clear_card) {
        fadeOutCard(cardElement, card.value, card.suit);
      }
    });
  }

  return cardElement;
}

// Probably also move to Python
function fadeOutCard(cardElement, value, suit) {
  cardElement.style.opacity = 0;
  setTimeout(() => {
    cardElement.style.display = "none";
  }, 400);
}

// Javascript to handle pop up rules window

const rulesModal = document.getElementById("rulesModal");
const closeButton = document.querySelector(".close-button");

closeButton.addEventListener("click", closeRulesModal);

function closeRulesModal() {
  rulesModal.style.display = "none";
}

function showRules() {
  menu.classList.remove('menu-open');
  rulesModal.style.display = "block";
}

// Show the rules modal when the page loads
// document.addEventListener("DOMContentLoaded", () => {
//   rulesModal.style.display = "block";
// });
