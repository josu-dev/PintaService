"strict";

/** @type {HTMLButtonElement} */
const openMainMenuButton = document.getElementById('openMainMenu');
/** @type {HTMLButtonElement} */
const closeMainMenuButton = document.getElementById('closeMainMenu');

/** @type {HTMLDivElement} */
const mainMenu = document.getElementById('mainMenuContainer');

openMainMenuButton.addEventListener('click', () => {
  mainMenu.classList.toggle('hidden');
});

closeMainMenuButton.addEventListener('click', () => {
  mainMenu.classList.toggle('hidden');
});
