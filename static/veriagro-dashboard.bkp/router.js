// ===============================
// router.js
// ===============================
import { renderDevicesPage } from './pages/devices.js';
import { renderUsersPage } from './pages/users.js';
import { renderSensorsPage } from './pages/sensors.js';
import { renderSensorDataPage } from './pages/sensorData.js';
import { renderTopicsPage } from './pages/topics.js';
import { renderCredentialsPage } from './pages/credentials.js';

const routes = {
    '#devices': renderDevicesPage,
    '#users': renderUsersPage,
    '#sensors': renderSensorsPage,
    '#sensordata': renderSensorDataPage,
    '#topics': renderTopicsPage,
    '#credentials': renderCredentialsPage
};

export function navigate() {
    const mainNav = document.getElementById('main-nav');
    const mainContent = document.getElementById('main-content');
    const hash = window.location.hash || '#devices';

    mainNav.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === hash);
    });

    mainContent.innerHTML = '';
    routes[hash]?.();
}

