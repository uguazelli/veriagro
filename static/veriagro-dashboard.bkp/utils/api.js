// ===============================
// utils/api.js
// ===============================
export async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('accessToken');
    const headers = { 'Authorization': `Bearer ${token}`, ...options.headers };
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        alert('Session expired. Please log in again.');
        localStorage.removeItem('accessToken');
        location.reload();
        throw new Error('Unauthorized');
    }
    return response;
}
