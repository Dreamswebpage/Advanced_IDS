const BACKEND_BASE = "http://127.0.0.1:5000";

const healthStatusEl = document.getElementById("health-status");
const refreshBtn = document.getElementById("refresh-btn");
const autoRefreshCheckbox = document.getElementById("auto-refresh");
const alertsBody = document.getElementById("alerts-body");

async function checkHealth() {
  try {
    const resp = await fetch(`${BACKEND_BASE}/api/health`);
    if (!resp.ok) throw new Error("Bad response");
    const data = await resp.json();
    healthStatusEl.textContent = `Backend OK • ${new Date(
      data.time * 1000
    ).toLocaleTimeString()}`;
    healthStatusEl.style.color = "#22c55e";
  } catch (e) {
    healthStatusEl.textContent = "Backend unreachable";
    healthStatusEl.style.color = "#f97373";
  }
}

function formatTime(ts) {
  return new Date(ts * 1000).toLocaleString();
}

function renderAlerts(alerts) {
  alertsBody.innerHTML = "";

  alerts.forEach((a) => {
    const tr = document.createElement("tr");

    const srcIp = a.details?.event?.src_ip || "-";
    const dstIp = a.details?.event?.dst_ip || "-";
    const rule = a.details?.rule || "-";

    tr.innerHTML = `
      <td>${a.id}</td>
      <td>${formatTime(a.timestamp)}</td>
      <td class="level-${a.level}">${a.level}</td>
      <td>${a.message}</td>
      <td>${srcIp}</td>
      <td>${dstIp}</td>
      <td>${rule}</td>
    `;

    alertsBody.appendChild(tr);
  });
}

async function fetchAlerts() {
  try {
    const resp = await fetch(`${BACKEND_BASE}/api/alerts?limit=100`);
    const data = await resp.json();
    renderAlerts(data);
  } catch (e) {
    console.error("Error fetching alerts:", e);
  }
}

refreshBtn.addEventListener("click", () => {
  fetchAlerts();
});

let autoRefreshInterval = null;

function setupAutoRefresh() {
  if (autoRefreshCheckbox.checked) {
    if (!autoRefreshInterval) {
      autoRefreshInterval = setInterval(fetchAlerts, 5000);
    }
  } else {
    if (autoRefreshInterval) {
      clearInterval(autoRefreshInterval);
      autoRefreshInterval = null;
    }
  }
}

autoRefreshCheckbox.addEventListener("change", setupAutoRefresh);

checkHealth();
fetchAlerts();
setupAutoRefresh();
