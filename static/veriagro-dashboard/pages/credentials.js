// ===============================
// pages/credentials.js (Extended with show-by-device)
// ===============================
import { fetchWithAuth } from '../utils/api.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

export function renderCredentialsPage() {
  const mainContent = document.getElementById('main-content');
  mainContent.innerHTML = `
    <h2 class="text-3xl font-bold mb-6 text-white">MQTT Credentials</h2>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Create New MQTT Credentials</h3>
      <form id="create-credential-form" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <input type="text" id="cred-device-id" placeholder="Device ID*" class="p-2 input-field rounded">
        <input type="text" id="cred-username" placeholder="MQTT Username*" class="p-2 input-field rounded">
        <input type="password" id="cred-password" placeholder="MQTT Password*" class="p-2 input-field rounded">
        <button type="submit" class="btn-primary p-2 rounded h-full">Create Credentials</button>
      </form>
    </div>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Find MQTT Credentials by Device ID</h3>
      <form id="find-credential-form" class="flex items-end gap-4">
        <input type="text" id="find-cred-device-id" placeholder="Enter Device ID" class="p-2 input-field rounded flex-grow">
        <button type="submit" class="btn-primary p-2 rounded h-full">Find Credentials</button>
      </form>
    </div>
    <div id="credentials-result"></div>
  `;

  document.getElementById('create-credential-form').addEventListener('submit', createCredential);
  document.getElementById('find-credential-form').addEventListener('submit', handleFindCredential);
}

async function createCredential(e) {
  e.preventDefault();
  const device_id = document.getElementById('cred-device-id').value;
  const mqtt_username = document.getElementById('cred-username').value;
  const mqtt_password_hash = document.getElementById('cred-password').value;

  if (!device_id || !mqtt_username || !mqtt_password_hash) return alert('All fields are required.');

  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/mqtt_credential/`, {
      method: 'POST',
      body: JSON.stringify({ device_id, mqtt_username, mqtt_password_hash })
    });
    if (response.status !== 201) {
      const err = await response.json();
      throw new Error(err.detail ? JSON.stringify(err.detail) : 'Failed to create credentials');
    }
    alert('MQTT Credentials created successfully!');
    e.target.reset();
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}

async function handleFindCredential(e) {
  e.preventDefault();
  const deviceId = document.getElementById('find-cred-device-id').value;
  if (!deviceId) return alert('Please enter a Device ID.');
  const resultBox = document.getElementById('credentials-result');
  resultBox.innerHTML = `<p class="text-center">Searching credentials for device <strong>${deviceId}</strong>...</p>`;

  try {
    const res = await fetchWithAuth(`${API_BASE_URL}/mqtt_credential/device/${deviceId}`);
    const creds = await res.json();

    if (!res.ok || !Array.isArray(creds) || creds.length === 0) {
      throw new Error('No credentials found.');
    }

    resultBox.innerHTML = creds.map(cred => `
  <div class="card p-4 mt-6">
    <h4 class="text-xl font-semibold mb-2">MQTT Credential</h4>
    <p><strong>ID:</strong> ${cred.id}</p>
    <p><strong>Device ID:</strong> ${cred.device_id}</p>
    <p><strong>Username:</strong> ${cred.mqtt_username}</p>
    <p><strong>Password Hash:</strong> ${cred.mqtt_password_hash}</p>
    <p><strong>Created At:</strong> ${cred.created_at}</p>
  </div>
`).join('');

  } catch (err) {
    resultBox.innerHTML = `<p class="text-red-500 mt-4">${err.message}</p>`;
  }
}
