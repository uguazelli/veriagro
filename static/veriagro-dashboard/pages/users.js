// ===============================
// pages/users.js
// ===============================
import { fetchWithAuth } from '../utils/api.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

export function renderUsersPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
    <h2 class="text-3xl font-bold mb-6 text-white">User Management</h2>
    <div class="card p-6 rounded-lg shadow-lg">
        <h3 class="text-xl font-semibold mb-4">Create New User</h3>
        <p class="text-sm text-gray-400 mb-4">The API does not support listing all users. You can create users and then retrieve them individually via other endpoints if needed.</p>
        <form id="create-user-form" class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
            <input type="email" id="user-email" placeholder="Email" class="p-2 input-field rounded">
            <input type="password" id="user-password" placeholder="Password" class="p-2 input-field rounded">
            <button type="submit" class="btn-primary p-2 rounded h-full">Create User</button>
        </form>
    </div>
  `;

    document.getElementById('create-user-form').addEventListener('submit', createUser);
}

async function createUser(e) {
    e.preventDefault();
    const email = document.getElementById('user-email').value;
    const password = document.getElementById('user-password').value;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/users/`, {
            method: 'POST',
            body: JSON.stringify({ email, password, role: "user" })
        });
        if (response.status !== 201) throw new Error('Failed to create user');
        alert('User created successfully!');
        e.target.reset();
    } catch (error) {
        alert(error.message);
    }
}
