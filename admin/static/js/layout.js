"strict";

/** @type {HTMLButtonElement} */
const openMainMenuButton = document.getElementById('openMainMenu');
/** @type {HTMLButtonElement} */
const closeMainMenuButton = document.getElementById('closeMainMenu');


/** @type {HTMLDivElement} */
const mainMenu = document.getElementById('mainMenuContainer');

/** @type {HTMLButtonElement} */
const openPerfil = document.getElementById('openPerfil');

/** @type {HTMLButtonElement} */
const closePerfil = document.getElementById('closePerfil');

/** @type {HTMLDivElement} */
const perfilContainer = document.getElementById('perfilContainer');

function clickOutsidePerfilMenu(event) {
  if ((!openPerfil.contains(event.target)) && (!perfilContainer.contains(event.target))) {
    perfilContainer.classList.add('hidden');
  }
}

openMainMenuButton.addEventListener('click', () => {
  mainMenu.classList.toggle('hidden');
});

closeMainMenuButton.addEventListener('click', () => {
  mainMenu.classList.toggle('hidden');
});

closePerfil.addEventListener('click', () => {
  perfilContainer.classList.toggle('hidden');
});

openPerfil.addEventListener('click', () => {
  perfilContainer.classList.toggle('hidden');
  document.addEventListener('click', (event) => clickOutsidePerfilMenu(event))
});
