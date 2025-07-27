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

async function loadTopics(deviceId) {
    const container = document.getElementById("topics-table-container");
    try {
        const res = await fetch(`${API_URL}/topics/device/${deviceId}`, {
            headers: { Authorization: `Bearer ${token}`, Accept: "application/json" }
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`Error ${res.status}: ${errorText}`);
        }

        const topics = await res.json();
        const normalized = Array.isArray(topics) ? topics : (topics ? [topics] : []);
        if (normalized.length === 0) {
            container.innerHTML = "<p class='text-muted'>No topics found.</p>";
            return;
        }

        const table = document.createElement("table");
        table.className = "table table-bordered table-responsive";
        table.innerHTML = `
            <thead><tr><th>ID</th><th>Topic</th><th>Direction</th><th>Created</th></tr></thead>
            <tbody>
                ${normalized.map(t => `
                    <tr>
                        <td>${t.id}</td>
                        <td>${t.topic}</td>
                        <td>${t.direction}</td>
                        <td>${new Date(t.created_at).toLocaleString()}</td>
                    </tr>`).join("")}
            </tbody>`;
        container.innerHTML = "";
        container.appendChild(table);
    } catch (e) {
        container.innerHTML = `<p class='text-danger'>Failed to load topics: ${e.message}</p>`;
    }
}



async function loadCredentials(deviceId) {
    const container = document.getElementById("credentials-table-container");
    try {
        const res = await fetch(`${API_URL}/mqtt_credential/device/${deviceId}`, {
            headers: { Authorization: `Bearer ${token}`, Accept: "application/json" }
        });
        const creds = await res.json();
        const normalized = Array.isArray(creds) ? creds : (creds ? [creds] : []);
        if (normalized.length === 0) {
            container.innerHTML = "<p class='text-muted'>No credentials found.</p>";
            return;
        }

        const table = document.createElement("table");
        table.className = "table table-bordered table-responsive";
        table.innerHTML = `
            <thead><tr><th>ID</th><th>Username</th><th>Created</th></tr></thead>
            <tbody>
                ${normalized.map(c => `
                    <tr>
                        <td>${c.id}</td>
                        <td>${c.mqtt_username}</td>
                        <td>${new Date(c.created_at).toLocaleString()}</td>
                    </tr>`).join("")}
            </tbody>`;
        container.innerHTML = "";
        container.appendChild(table);
    } catch (e) {
        container.innerHTML = `<p class='text-danger'>Failed to load credentials: ${e.message}</p>`;
    }
}

async function handleTopicFormSubmit(e) {
    e.preventDefault();

    const body = {
        topic: document.getElementById("topic").value.trim(),
        direction: document.getElementById("direction").value,
        device_id: currentDeviceId
    };

    if (!body.topic || !body.direction) {
        alert("Topic and Direction are required");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/topics/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        if (!res.ok) throw new Error(await res.text());

        document.getElementById("topic-form").reset();
        await loadTopics(currentDeviceId);

    } catch (err) {
        alert(`Failed to add topic: ${err.message}`);
    }
}


async function handleCredentialFormSubmit(e) {
    e.preventDefault();
    const body = {
        device_id: currentDeviceId,
        mqtt_username: document.getElementById("mqtt_username").value.trim(),
        mqtt_password_hash: document.getElementById("mqtt_password_hash").value.trim()
    };
    if (!body.mqtt_username || !body.mqtt_password_hash) {
        alert("Username and Password are required");
        return;
    }
    try {
        const res = await fetch(`${API_URL}/mqtt_credential/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(await res.text());
        document.getElementById("credential-form").reset();
        await loadCredentials(currentDeviceId);
    } catch (err) {
        alert(`Failed to add credentials: ${err.message}`);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    requireAuth();
    currentDeviceId = getDeviceIdFromPath();
    if (!currentDeviceId) return;
    document.getElementById("page-title").innerText = `MQTT Topics for Device: ${currentDeviceId}`;
    document.getElementById("topic-form").addEventListener("submit", handleTopicFormSubmit);
    document.getElementById("credential-form").addEventListener("submit", handleCredentialFormSubmit);
    loadTopics(currentDeviceId);
    loadCredentials(currentDeviceId);
});
