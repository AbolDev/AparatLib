document.addEventListener("DOMContentLoaded", function() {
    const button = document.createElement('button');
    button.id = 'theme-toggle-button';
    button.textContent = 'Toggle Theme';
    document.body.appendChild(button);

    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);

    button.addEventListener('click', function() {
        const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});
