// ===============================
// main.js (Entry point)
// ===============================
import { navigate } from './router.js';
import { setupAuth } from './utils/auth.js';

window.addEventListener('hashchange', navigate);

document.addEventListener('DOMContentLoaded', () => {
    const loginPage = document.getElementById('login-page');
    const dashboard = document.getElementById('dashboard');

    if (localStorage.getItem('accessToken')) {
        loginPage.style.display = 'none';
        dashboard.style.display = 'block';
        navigate();
    } else {
        loginPage.style.display = 'flex';
        dashboard.style.display = 'none';
    }

    setupAuth();
});

