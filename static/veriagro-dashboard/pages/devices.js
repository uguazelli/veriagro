// ===============================
// pages/devices.js
// ===============================
import { fetchWithAuth } from '../utils/api.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

export function renderDevicesPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
    <h2 class="text-3xl font-bold mb-6 text-white">Device Management</h2>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
        <h3 class="text-xl font-semibold mb-4">Register New Device</h3>
        <form id="create-device-form" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <input type="text" id="device-name" placeholder="Device Name" class="p-2 input-field rounded">
            <input type="text" id="device-model" placeholder="Model" class="p-2 input-field rounded">
            <input type="text" id="device-serial" placeholder="Serial Number" class="p-2 input-field rounded">
            <button type="submit" class="btn-primary p-2 rounded h-full">Register Device</button>
        </form>
    </div>
    <div id="devices-list" class="mt-8"></div>
  `;

    document.getElementById('create-device-form').addEventListener('submit', createDevice);
    loadDevices();
}

async function createDevice(e) {
    e.preventDefault();
    const name = document.getElementById('device-name').value;
    const model = document.getElementById('device-model').value;
    const serial_number = document.getElementById('device-serial').value;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/devices/`, {
            method: 'POST',
            body: JSON.stringify({ name, model, serial_number })
        });
        if (response.status !== 201) throw new Error('Failed to create device');
        alert('Device registered successfully!');
        e.target.reset();
        loadDevices();
    } catch (error) {
        alert(error.message);
    }
}

async function loadDevices() {
    const list = document.getElementById('devices-list');
    list.innerHTML = `<p class="text-center">Loading devices...</p>`;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/devices/`);
        const devices = await response.json();
        if (devices.length === 0) {
            list.innerHTML = `<p class="text-center text-gray-400">No devices found. Register one above to get started.</p>`;
            return;
        }
        list.innerHTML = `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      ${devices.map(deviceCard).join('')}
    </div>`;
    } catch (error) {
        list.innerHTML = `<p class="text-center text-red-400">Failed to load devices.</p>`;
    }
}

function deviceCard(device) {
    return `
    <div class="card p-4 rounded-lg shadow-lg flex flex-col justify-between">
      <div>
        <h4 class="font-bold text-lg">${device.name}</h4>
        <p class="text-xs text-gray-500 mb-2 break-all">${device.id}</p>
        <p class="text-sm">Model: ${device.model || 'N/A'}</p>
        <p class="text-sm">S/N: ${device.serial_number || 'N/A'}</p>
        <p class="text-sm">Last Seen: ${device.last_seen ? new Date(device.last_seen).toLocaleString() : 'Never'}</p>
      </div>
      <div class="mt-4 flex justify-end">
        <button onclick="deleteDevice('${device.id}')" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">Delete</button>
      </div>
    </div>
  `;
}

window.deleteDevice = async function (deviceId) {
    if (!confirm('Are you sure you want to delete this device? This will also orphan its sensors.')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/devices/${deviceId}`, { method: 'DELETE' });
        if (response.status !== 204) throw new Error('Failed to delete device');
        alert('Device deleted successfully');
        loadDevices();
    } catch (error) {
        alert(error.message);
    }
};