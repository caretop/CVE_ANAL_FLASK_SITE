# CISA KEV Dashboard (Flask)

Flask backend + dashboard for the CISA Known Exploited Vulnerabilities (KEV) catalog.
Serves KPI/aggregation/search JSON APIs from a pandas-processed dataset, and renders
a dashboard, a searchable vulnerability list, and a CVE detail page.

The data layer works off **either CSV or MongoDB** — controlled by one env var.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py   # http://localhost:5000
```

## Data source

Set `DATA_SOURCE` in `.env`:

- `csv` (default) — reads `data/known_exploited_vulnerabilities.csv` (path configurable
  via `KEV_CSV_PATH`).
- `mongo` — reads from MongoDB (`MONGO_URI` / `MONGO_DB` / `MONGO_COLLECTION`).
  Load the CSV into Mongo first:

  ```bash
  python scripts/import_to_mongo.py
  ```

Either way, `analysis/kev_analysis.py` loads the raw rows into a pandas DataFrame and
builds the same derived columns (`responseDays`, `year`, `month`, `ransomwareFlag`,
`cweCount`, …), so every API endpoint behaves identically regardless of source.

## Project layout

```
app.py                  Flask app factory / entrypoint
config.py                DATA_SOURCE / CSV / Mongo settings
analysis/kev_analysis.py  CSV or MongoDB loading, preprocessing, aggregation, search
routes/main.py            Page routes (/, /vulnerabilities, /vulnerability/<cve>)
routes/api.py              JSON API routes (/api/...)
scripts/import_to_mongo.py Loads the CSV into MongoDB
templates/                 index.html, vulnerabilities.html, detail.html (+ base.html)
static/css/style.css
static/js/dashboard.js     Dashboard charts (Chart.js, vendored under static/js/vendor)
static/js/vulnerabilities.js  Search / filter / paginated table
static/js/detail.js        CVE detail rendering
data/known_exploited_vulnerabilities.csv  CISA KEV catalog export
```

## API

| Endpoint | Description |
|---|---|
| `GET /api/summary` | KPI totals |
| `GET /api/trends` | Monthly KEV registration counts |
| `GET /api/vendors?limit=10` | Top vendors by CVE count |
| `GET /api/products?limit=10` | Top products by CVE count |
| `GET /api/cwes?limit=10` | Top CWEs by CVE count |
| `GET /api/ransomware` | Known vs Unknown ransomware counts |
| `GET /api/response-time` | Response-time (dueDate - dateAdded) histogram buckets |
| `GET /api/filters` | Distinct vendors/years, for the search page dropdowns |
| `GET /api/vulnerabilities?keyword=&vendor=&ransomware=&year=` | Search/filter |
| `GET /api/vulnerabilities/<cveID>` | Full detail for one CVE (404 if unknown) |
