const token = localStorage.getItem("accessToken");

async function loadDevices() {
  try {
    const res = await fetch(`${API_URL}/devices/`, {
      headers: { Authorization: `Bearer ${token}`, Accept: "application/json" }
    });
    const data = await res.json();
    renderDevices(data);
  } catch (e) {
    console.error("Error loading devices", e);
  }
}

function renderDevices(devices) {
  const container = document.getElementById("devices-table-container");
  const table = document.createElement("table");
  table.className = "table table-striped";
  table.innerHTML = `
        <thead>
          <tr><th>Name</th><th>Model</th><th>Serial</th><th>Location</th><th>Lat</th><th>Long</th><th>Sensors</th><th>Topics</th></tr>
        </thead>
        <tbody>
          ${devices.map(d => `
            <tr data-id="${d.id}">
              <td>${d.name}</td>
              <td>${d.model}</td>
              <td>${d.serial_number}</td>
              <td>${d.location}</td>
              <td>${d.latitude}</td>
              <td>${d.longitude}</td>
              <td><a href="/sensor-settings/${d.id}">View</a></td>
              <td><a href="/topics-settings/${d.id}">View</a></td>
            </tr>
          `).join("")}
        </tbody>
      `;

  const wrapper = document.createElement("div");
  wrapper.className = "table-responsive";
  wrapper.appendChild(table);
  container.innerHTML = "";
  container.appendChild(wrapper);
}

async function handleDeviceFormSubmit(e) {
  e.preventDefault();
  const body = {
    name: document.getElementById("name").value.trim(),
    model: document.getElementById("model").value.trim(),
    serial_number: document.getElementById("serial_number").value.trim(),
    location: document.getElementById("location").value.trim(),
    latitude: parseFloat(document.getElementById("latitude").value.trim()),
    longitude: parseFloat(document.getElementById("longitude").value.trim())
  };

  if (!body.name || !body.model || !body.serial_number) {
    alert("Please fill in at least name, model, and serial number.");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/devices/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify(body)
    });

    if (!res.ok) throw new Error(await res.text());
    document.getElementById("device-form").reset();
    await loadDevices(); // Refresh device list
  } catch (err) {
    alert(`Failed to add device: ${err.message}`);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  requireAuth();
  loadDevices();
  document.getElementById("device-form").addEventListener("submit", handleDeviceFormSubmit);
});
