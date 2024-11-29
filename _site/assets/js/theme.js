
const toggleTheme = document.getElementById('theme-toggle');
toggleTheme.addEventListener('click', () => {
    document.body.classList.toggle('light');
    const theme = document.body.classList.contains('light') ? 'light' : 'dark';
    localStorage.setItem('theme', theme);
});

window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light');
    }
});
            