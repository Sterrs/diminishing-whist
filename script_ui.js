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