let currentDeviceId = null;
function getDeviceIdFromPath() {
    const parts = window.location.pathname.split('/');
    const id = parts[parts.length - 1];
    if (!id || id.length < 10) {
        alert("Missing device ID");
        return null;
    }
    return id;
}
async function loadSensors(deviceId) {
    const container = document.getElementById("sensors-table-container");
    try {
        const res = await fetch(`${API_URL}/sensors/device/${deviceId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
                Accept: "application/json"
            }
        });

        const sensors = await res.json();
        if (!sensors.length) {
            container.innerHTML = "<p class='text-muted'>No sensors found.</p>";
            return;
        }

        const table = document.createElement("table");
        table.className = "table table-bordered table-responsive";

        table.innerHTML = `
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Type</th>
              <th>Model</th>
              <th>Manufacturer</th>
              <th>Model ID</th>
              <th>Config</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            ${sensors.map(s => `
              <tr>
                <td>${s.id}</td>
                <td>${s.name}</td>
                <td>${s.type}</td>
                <td>${s.model}</td>
                <td>${s.manufacturer}</td>
                <td>${s.model_id}</td>
                <td><pre>${JSON.stringify(s.config, null, 2)}</pre></td>
                <td>${new Date(s.created_at).toLocaleString()}</td>
              </tr>
            `).join("")}
          </tbody>
        `;

        container.innerHTML = "";
        container.appendChild(table);
    } catch (e) {
        container.innerHTML = `<p class='text-danger'>Failed to load sensors: ${e.message}</p>`;
    }
}



async function loadSensorData(deviceId) {
    const container = document.getElementById("sensor-data-table-container");
    try {
        const res = await fetch(`${API_URL}/sensor_data/device/${deviceId}?limit=1000`, {
            headers: { Authorization: `Bearer ${token}`, Accept: "application/json" }
        });
        const data = await res.json();
        if (!data.length) {
            container.innerHTML = "<p class='text-muted'>No sensor data available.</p>";
            return;
        }
        const table = document.createElement("table");
        table.className = "table table-hover table-responsive";
        table.innerHTML = `<thead><tr>
            <th>Sensor ID</th><th>Unit</th><th>Value</th><th>Status</th><th>Timestamp</th>
          </tr></thead><tbody>${data.map(d => `<tr>
              <td>${d.sensor_id}</td><td>${d.unit}</td><td>${d.value}</td><td>${d.status}</td><td>${new Date(d.timestamp).toLocaleString()}</td>
            </tr>`).join("")
            }</tbody>`;
        container.innerHTML = "";
        container.appendChild(table);
    } catch (e) {
        container.innerHTML = `<p class='text-danger'>Failed to load sensor data: ${e.message}</p>`;
    }
}
async function handleSensorFormSubmit(e) {
    e.preventDefault();

    const body = {
        name: document.getElementById("sensor_name").value.trim(),
        type: document.getElementById("sensor_type").value.trim(),
        model: document.getElementById("sensor_model").value.trim(),
        manufacturer: document.getElementById("sensor_manufacturer").value.trim(),
        model_id: document.getElementById("sensor_model_id").value.trim(),
        device_id: currentDeviceId
    };

    try {
        const configRaw = document.getElementById("sensor_config").value.trim();
        body.config = configRaw ? JSON.parse(configRaw) : {};
    } catch (err) {
        alert("Invalid JSON in config field");
        return;
    }

    if (!body.name || !body.type || !body.model_id) {
        alert("Name, Type, and Model ID are required.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/sensors/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(errorText);
        }

        document.getElementById("sensor-form").reset();
        await loadSensors(currentDeviceId);
    } catch (err) {
        alert(`Failed to add sensor: ${err.message}`);
    }
}



document.addEventListener("DOMContentLoaded", () => {
    requireAuth();
    currentDeviceId = getDeviceIdFromPath();
    if (!currentDeviceId) return;
    document.getElementById("page-title").innerText = `Sensors for Device: ${currentDeviceId}`;
    document.getElementById("sensor-form").addEventListener("submit", handleSensorFormSubmit);
    loadSensors(currentDeviceId);
    loadSensorData(currentDeviceId);
});
