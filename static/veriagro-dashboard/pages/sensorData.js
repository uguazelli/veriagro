// ===============================
// pages/sensorData.js
// ===============================
import { fetchWithAuth } from '../utils/api.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

export function renderSensorDataPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
    <h2 class="text-3xl font-bold mb-6 text-white">Sensor Data History</h2>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Fetch Sensor Data</h3>
      <p class="text-sm text-gray-400 mb-4">Find all data submitted by a specific Device or an individual Sensor.</p>
      <form id="find-data-form" class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <input type="text" id="data-device-id" placeholder="Device ID (for all its sensors)" class="p-2 input-field rounded">
        <input type="text" id="data-sensor-id" placeholder="OR Sensor ID (for one sensor)" class="p-2 input-field rounded">
        <input type="number" id="data-limit" placeholder="Limit (e.g., 100)" class="p-2 input-field rounded">
        <button type="submit" class="btn-primary p-2 rounded h-full col-span-1 md:col-span-3">Fetch Data</button>
      </form>
    </div>
    <div id="sensor-data-list" class="mt-8"></div>
  `;

    document.getElementById('find-data-form').addEventListener('submit', handleFindSensorData);
}

async function handleFindSensorData(e) {
    e.preventDefault();
    const deviceId = document.getElementById('data-device-id').value;
    const sensorId = document.getElementById('data-sensor-id').value;
    const limit = document.getElementById('data-limit').value || 1000;
    const list = document.getElementById('sensor-data-list');
    list.innerHTML = `<p class="text-center">Fetching data...</p>`;

    if (!deviceId && !sensorId) {
        list.innerHTML = `<p class="text-center text-red-400">Please provide a Device ID or a Sensor ID.</p>`;
        return;
    }

    const url = sensorId
        ? `${API_BASE_URL}/sensor_data/sensor/${sensorId}?limit=${limit}`
        : `${API_BASE_URL}/sensor_data/device/${deviceId}?limit=${limit}`;

    try {
        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch sensor data.');
        const data = await response.json();

        if (!data || data.length === 0) {
            list.innerHTML = `<h3 class="text-xl font-semibold my-4">Results</h3><p class="text-center text-gray-400">No data found for the specified ID.</p>`;
            return;
        }

        list.innerHTML = `
      <h3 class="text-2xl font-semibold mb-4">Data Results</h3>
      <div class="card p-4 rounded-lg overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="border-b border-gray-600">
              <th class="p-2">Timestamp</th><th class="p-2">Sensor ID</th><th class="p-2">Value</th><th class="p-2">Unit</th>
            </tr>
          </thead>
          <tbody>
            ${data.map(dataRow).join('')}
          </tbody>
        </table>
      </div>
    `;
    } catch (error) {
        list.innerHTML = `<p class="text-center text-red-400">${error.message}</p>`;
    }
}

function dataRow(d) {
    return `
    <tr class="border-b border-gray-700">
      <td class="p-2">${new Date(d.created_at || d.timestamp).toLocaleString()}</td>
      <td class="p-2 text-xs font-mono break-all">${d.sensor_id}</td>
      <td class="p-2 font-bold">${d.value}</td>
      <td class="p-2">${d.unit}</td>
    </tr>
  `;
}
