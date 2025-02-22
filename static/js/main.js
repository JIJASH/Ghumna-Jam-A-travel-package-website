// // Dark Mode Toggle
// const themeButton = document.getElementById('theme-button');
// const darkTheme = 'dark-theme';
// const iconTheme = 'ri-sun-line';

// // Check if the user previously selected a theme
// const selectedTheme = localStorage.getItem('selected-theme');
// const selectedIcon = localStorage.getItem('selected-icon');

// if (selectedTheme) {
//     document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme);
//     themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme);
// }

// // Toggle theme on button click
// themeButton.addEventListener('click', () => {
//     document.body.classList.toggle(darkTheme);
//     themeButton.classList.toggle(iconTheme);
//     localStorage.setItem('selected-theme', document.body.classList.contains(darkTheme) ? 'dark' : 'light');
//     localStorage.setItem('selected-icon', themeButton.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line');
// });