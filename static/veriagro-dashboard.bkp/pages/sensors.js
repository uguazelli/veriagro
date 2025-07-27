// ===============================
// pages/sensors.js
// ===============================
import { fetchWithAuth } from '../utils/api.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

export function renderSensorsPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
    <h2 class="text-3xl font-bold mb-6 text-white">Sensor Management</h2>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Find Sensors by Device ID</h3>
      <form id="find-sensors-form" class="flex items-end gap-4">
        <div class="flex-grow">
          <label for="find-device-id" class="text-sm text-gray-400">Device ID</label>
          <input type="text" id="find-device-id" placeholder="Enter Device ID to find its sensors" class="w-full mt-1 p-2 input-field rounded">
        </div>
        <button type="submit" class="btn-primary p-2 rounded h-10">Find Sensors</button>
      </form>
    </div>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Create New Sensor</h3>
      <form id="create-sensor-form" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 items-end">
        <input type="text" id="sensor-device-id" placeholder="Device ID*" class="p-2 input-field rounded">
        <input type="text" id="sensor-name" placeholder="Sensor Name" class="p-2 input-field rounded">
        <input type="text" id="sensor-type" placeholder="Type" class="p-2 input-field rounded">
        <input type="text" id="sensor-model" placeholder="Model" class="p-2 input-field rounded">
        <input type="text" id="sensor-manufacturer" placeholder="Manufacturer" class="p-2 input-field rounded">
        <button type="submit" class="btn-primary p-2 rounded h-full">Create Sensor</button>
      </form>
    </div>
    <div id="sensors-list" class="mt-8"></div>
  `;

    document.getElementById('find-sensors-form').addEventListener('submit', handleFindSensors);
    document.getElementById('create-sensor-form').addEventListener('submit', createSensor);
}

async function handleFindSensors(e) {
    e.preventDefault();
    const deviceId = document.getElementById('find-device-id').value;
    if (!deviceId) return alert('Please enter a Device ID.');
    loadSensors(deviceId);
}

async function loadSensors(deviceId) {
    const list = document.getElementById('sensors-list');
    list.innerHTML = `<p class="text-center">Loading sensors for device ${deviceId}...</p>`;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/sensors/device/${deviceId}`);
        if (!response.ok) {
            if (response.status === 404) throw new Error(`No sensors found for Device ID: ${deviceId}`);
            throw new Error('Failed to fetch sensors.');
        }
        const sensorData = await response.json();
        const sensors = Array.isArray(sensorData) ? sensorData : [sensorData];
        if (sensors.length === 0 || !sensors[0]) {
            list.innerHTML = `<h3 class="text-xl font-semibold my-4">Results</h3><p class="text-center text-gray-400">No sensors found for device ${deviceId}.</p>`;
            return;
        }
        list.innerHTML = `
      <h3 class="text-2xl font-semibold mb-4">Sensors for Device <span class="text-green-400 text-base break-all">${deviceId}</span></h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        ${sensors.map(sensorCard).join('')}
      </div>
    `;
    } catch (error) {
        list.innerHTML = `<h3 class="text-xl font-semibold my-4">Results</h3><p class="text-center text-red-400">${error.message}</p>`;
    }
}

function sensorCard(sensor) {
    return `
    <div class="card p-4 rounded-lg shadow-lg flex flex-col justify-between">
      <div>
        <h4 class="font-bold text-lg">${sensor.name || 'N/A'} <span class="text-sm font-light text-gray-400">(${sensor.type || 'N/A'})</span></h4>
        <p class="text-xs text-gray-500 mb-2 break-all">${sensor.id}</p>
        <p class="text-sm">Model: ${sensor.model || 'N/A'}</p>
        <p class="text-sm">Manufacturer: ${sensor.manufacturer || 'N/A'}</p>
      </div>
      <div class="mt-4 flex justify-end">
        <button onclick="deleteSensor('${sensor.id}', '${sensor.device_id}')" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">Delete</button>
      </div>
    </div>
  `;
}

async function createSensor(e) {
    e.preventDefault();
    const device_id = document.getElementById('sensor-device-id').value;
    const name = document.getElementById('sensor-name').value;
    const type = document.getElementById('sensor-type').value;
    const model = document.getElementById('sensor-model').value;
    const manufacturer = document.getElementById('sensor-manufacturer').value;
    if (!device_id) return alert('Device ID is required to create a sensor.');
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/sensors/`, {
            method: 'POST',
            body: JSON.stringify({ device_id, name, type, model, manufacturer })
        });
        if (response.status !== 201) throw new Error('Failed to create sensor');
        alert('Sensor created successfully!');
        document.getElementById('create-sensor-form').reset();
        loadSensors(device_id);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

window.deleteSensor = async function (sensorId, deviceId) {
    if (!confirm('Are you sure you want to delete this sensor?')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/sensors/${sensorId}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to delete sensor');
        alert('Sensor deleted successfully');
        loadSensors(deviceId);
    } catch (error) {
        alert(error.message);
    }
};
