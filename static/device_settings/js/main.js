// Shared functions
var token = null

function requireAuth() {
    token = localStorage.getItem("accessToken");
    if (!token) window.location.href = "/login";
}
const API_URL = "http://localhost:8000";

