const CHART_COLORS = {
  accent: "#38bdf8",
  accent2: "#f97316",
  grid: "rgba(148, 163, 184, 0.15)",
  text: "#94a3b8",
  palette: [
    "#38bdf8", "#f97316", "#a78bfa", "#34d399", "#fbbf24",
    "#f87171", "#60a5fa", "#4ade80", "#f472b6", "#facc15",
  ],
};

Chart.defaults.color = CHART_COLORS.text;
Chart.defaults.borderColor = CHART_COLORS.grid;
Chart.defaults.font.family = "'Segoe UI', 'Malgun Gothic', sans-serif";

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${url}`);
  return res.json();
}

function setKPI(id, value) {
  document.getElementById(id).textContent = value;
}

async function loadSummary() {
  const data = await fetchJSON("/api/summary");
  setKPI("kpi-total", data.total.toLocaleString());
  setKPI("kpi-vendors", data.vendors.toLocaleString());
  setKPI("kpi-products", data.products.toLocaleString());
  setKPI("kpi-ransomware", data.ransomwareKnown.toLocaleString());
  setKPI("kpi-response", `${data.averageResponseDays}`);
}

async function loadTrends() {
  const data = await fetchJSON("/api/trends");
  new Chart(document.getElementById("chart-trends"), {
    type: "line",
    data: {
      labels: data.map((d) => d.month),
      datasets: [{
        label: "KEV 등록 수",
        data: data.map((d) => d.count),
        borderColor: CHART_COLORS.accent,
        backgroundColor: "rgba(56, 189, 248, 0.15)",
        fill: true,
        tension: 0.3,
        pointRadius: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true, grid: { color: CHART_COLORS.grid } },
      },
    },
  });
}

async function loadHorizontalBar(canvasId, url, labelKey, countKey, label) {
  const data = await fetchJSON(`${url}?limit=10`);
  new Chart(document.getElementById(canvasId), {
    type: "bar",
    data: {
      labels: data.map((d) => d[labelKey]),
      datasets: [{
        label,
        data: data.map((d) => d[countKey]),
        backgroundColor: CHART_COLORS.accent2,
        borderRadius: 4,
      }],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { beginAtZero: true, grid: { color: CHART_COLORS.grid } },
        y: { grid: { display: false } },
      },
    },
  });
}

async function loadRansomware() {
  const data = await fetchJSON("/api/ransomware");
  new Chart(document.getElementById("chart-ransomware"), {
    type: "doughnut",
    data: {
      labels: data.map((d) => d.status),
      datasets: [{
        data: data.map((d) => d.count),
        backgroundColor: CHART_COLORS.palette,
        borderColor: "#1e293b",
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom" } },
    },
  });
}

async function loadResponseTime() {
  const data = await fetchJSON("/api/response-time");
  new Chart(document.getElementById("chart-response-time"), {
    type: "bar",
    data: {
      labels: data.map((d) => `${d.range}일`),
      datasets: [{
        label: "CVE 수",
        data: data.map((d) => d.count),
        backgroundColor: CHART_COLORS.accent,
        borderRadius: 4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true, grid: { color: CHART_COLORS.grid } },
      },
    },
  });
}

async function initDashboard() {
  try {
    await Promise.all([
      loadSummary(),
      loadTrends(),
      loadHorizontalBar("chart-vendors", "/api/vendors", "vendor", "count", "벤더별 CVE 수"),
      loadHorizontalBar("chart-products", "/api/products", "product", "count", "제품별 CVE 수"),
      loadHorizontalBar("chart-cwes", "/api/cwes", "cwe", "count", "CWE별 CVE 수"),
      loadRansomware(),
      loadResponseTime(),
    ]);
  } catch (err) {
    console.error(err);
  }
}

initDashboard();
