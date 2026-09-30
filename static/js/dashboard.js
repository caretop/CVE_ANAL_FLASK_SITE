// 대시보드 KPI 숫자만 채웁니다. 차트/시각화는 별도 파트에서 구현 예정이며,
// 필요한 데이터는 /api/summary, /api/trends, /api/vendors, /api/products,
// /api/cwes, /api/ransomware, /api/response-time 에서 이미 제공됩니다.

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`요청 실패: ${url}`);
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

loadSummary().catch((err) => console.error(err));
