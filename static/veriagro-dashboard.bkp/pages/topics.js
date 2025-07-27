// ===============================
// pages/topics.js
// ===============================
import { fetchWithAuth } from '../utils/api.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

export function renderTopicsPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
    <h2 class="text-3xl font-bold mb-6 text-white">MQTT Topics</h2>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Find Topics by Device ID</h3>
      <form id="find-topics-form" class="flex items-end gap-4">
        <div class="flex-grow">
          <label for="find-topics-device-id" class="text-sm text-gray-400">Device ID</label>
          <input type="text" id="find-topics-device-id" placeholder="Enter Device ID to find its topics" class="w-full mt-1 p-2 input-field rounded">
        </div>
        <button type="submit" class="btn-primary p-2 rounded h-10">Find Topics</button>
      </form>
    </div>
    <div class="card p-6 rounded-lg shadow-lg mb-6">
      <h3 class="text-xl font-semibold mb-4">Create New Topic</h3>
      <form id="create-topic-form" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <input type="text" id="topic-device-id" placeholder="Device ID*" class="p-2 input-field rounded">
        <input type="text" id="topic-string" placeholder="Topic (e.g., /data/temp)*" class="p-2 input-field rounded">
        <select id="topic-direction" class="p-2 input-field rounded h-10">
          <option value="publish">Publish</option>
          <option value="subscribe">Subscribe</option>
        </select>
        <button type="submit" class="btn-primary p-2 rounded h-full">Create Topic</button>
      </form>
    </div>
    <div id="topics-list" class="mt-8"></div>
  `;

    document.getElementById('find-topics-form').addEventListener('submit', handleFindTopics);
    document.getElementById('create-topic-form').addEventListener('submit', createTopic);
}

async function handleFindTopics(e) {
    e.preventDefault();
    const deviceId = document.getElementById('find-topics-device-id').value;
    if (!deviceId) return alert('Please enter a Device ID.');
    loadTopics(deviceId);
}

async function loadTopics(deviceId) {
    const list = document.getElementById('topics-list');
    list.innerHTML = `<p class="text-center">Loading topics for device ${deviceId}...</p>`;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/topics/device/${deviceId}`);
        if (!response.ok) throw new Error('Failed to fetch topics.');
        const topics = await response.json();

        if (topics.length === 0) {
            list.innerHTML = `<h3 class="text-xl font-semibold my-4">Results</h3><p class="text-center text-gray-400">No topics found for device ${deviceId}.</p>`;
            return;
        }

        list.innerHTML = `
      <h3 class="text-2xl font-semibold mb-4">Topics for Device <span class="text-green-400 text-base break-all">${deviceId}</span></h3>
      <div class="card p-4 rounded-lg overflow-x-auto">
        <table class="w-full text-left">
          <thead><tr class="border-b border-gray-600"><th class="p-2">Topic</th><th class="p-2">Direction</th><th class="p-2">Actions</th></tr></thead>
          <tbody>
            ${topics.map(topicRow).join('')}
          </tbody>
        </table>
      </div>
    `;
    } catch (error) {
        list.innerHTML = `<h3 class="text-xl font-semibold my-4">Results</h3><p class="text-center text-red-400">${error.message}</p>`;
    }
}

function topicRow(topic) {
    return `
    <tr class="border-b border-gray-700">
      <td class="p-2 font-mono">${topic.topic}</td>
      <td class="p-2"><span class="px-2 py-1 text-xs rounded-full ${topic.direction === 'publish' ? 'bg-blue-500 text-white' : 'bg-purple-500 text-white'}">${topic.direction}</span></td>
      <td class="p-2"><button onclick="deleteTopic('${topic.id}', '${topic.device_id}')" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">Delete</button></td>
    </tr>
  `;
}

async function createTopic(e) {
    e.preventDefault();
    const device_id = document.getElementById('topic-device-id').value;
    const topic = document.getElementById('topic-string').value;
    const direction = document.getElementById('topic-direction').value;

    if (!device_id || !topic) return alert('Device ID and Topic are required.');
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/topics/`, {
            method: 'POST',
            body: JSON.stringify({ device_id, topic, direction })
        });
        if (response.status !== 201) throw new Error('Failed to create topic');
        alert('Topic created successfully!');
        document.getElementById('create-topic-form').reset();
        loadTopics(device_id);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

window.deleteTopic = async function (topicId, deviceId) {
    if (!confirm('Are you sure you want to delete this topic?')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/topics/${topicId}`, { method: 'DELETE' });
        if (response.status !== 204) throw new Error('Failed to delete topic');
        alert('Topic deleted successfully');
        loadTopics(deviceId);
    } catch (error) {
        alert(error.message);
    }
};
