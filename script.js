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

// Javascript to handle pop up rules window

const rulesModal = document.getElementById("rulesModal");
const aboutModal = document.getElementById("aboutModal")
const closeButton = document.querySelector(".close-button");
const aboutCloseButton = document.querySelector(".about-close-button");

closeButton.addEventListener("click", closeRulesModal);
aboutCloseButton.addEventListener("click", closeRulesModal);

function closeRulesModal() {
  rulesModal.style.display = "none";
  aboutModal.style.display = "none";
}

function showRules() {
  menu.classList.remove('menu-open');
  rulesModal.style.display = "block";
}

function showAbout() {
  menu.classList.remove('menu-open');
  aboutModal.style.display = "block";
}

// Show the rules modal when the page loads
// document.addEventListener("DOMContentLoaded", () => {
//   rulesModal.style.display = "block";
// });
