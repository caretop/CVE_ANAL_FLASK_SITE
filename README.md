# CISA KEV Dashboard (Flask)

데스크탑에서 바로 돌리는 단순한 Flask 서버입니다. CISA Known Exploited Vulnerabilities
(KEV) 카탈로그를 pandas로 가공해 KPI/집계/검색 JSON API로 제공하고, 대시보드/검색
목록/CVE 상세 페이지를 렌더링합니다. 사이트 UI는 한국어입니다.

**대시보드의 차트/시각화 영역은 의도적으로 빈 틀(placeholder)입니다.** 실제 차트
구현은 별도 파트에서 진행하며, 각 영역이 쓸 데이터는 `/api/...` 엔드포인트에서 이미
제공됩니다 (아래 API 표 참고). `templates/index.html`의 `.chart-placeholder`
영역에 원하는 라이브러리로 차트를 붙이면 됩니다.

## 실행 방법 (데스크탑)

```bash
python3 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py   # http://localhost:5000
```

MongoDB 없이도 바로 실행됩니다 (아래 참고).

## 데이터 소스: CSV 기본 + MongoDB 폴백

`.env`의 `DATA_SOURCE`로 제어합니다.

- `csv` (기본값) — `data/known_exploited_vulnerabilities.csv`(경로는 `KEV_CSV_PATH`로 조정 가능)에서 읽습니다.
  **CSV 파일이 없거나 비어 있으면 자동으로 MongoDB(`MONGO_URI`/`MONGO_DB`/`MONGO_COLLECTION`)로 폴백**합니다.
- `mongo` — MongoDB만 사용하도록 강제합니다.

MongoDB를 쓰려면 먼저 CSV를 한 번 적재하세요:

```bash
python scripts/import_to_mongo.py
```

어느 쪽이든 `analysis/kev_analysis.py`가 원본 행을 pandas DataFrame으로 읽어 동일한
파생 컬럼(`responseDays`, `year`, `month`, `ransomwareFlag`, `cweCount` 등)을 만들기
때문에, API 응답은 데이터 소스와 무관하게 동일합니다.

## 프로젝트 구조

```
app.py                     Flask 앱 생성/실행 엔트리포인트
config.py                  DATA_SOURCE / CSV / Mongo 설정
analysis/kev_analysis.py   CSV 또는 MongoDB 로딩, 전처리, 집계, 검색 로직
routes/main.py             페이지 라우트 (/, /vulnerabilities, /vulnerability/<cve>)
routes/api.py              JSON API 라우트 (/api/...)
scripts/import_to_mongo.py CSV를 MongoDB로 적재하는 스크립트
templates/                 index.html, vulnerabilities.html, detail.html (+ base.html)
static/css/style.css
static/js/dashboard.js         대시보드 KPI 숫자만 채움 (차트는 빈 틀)
static/js/vulnerabilities.js   검색 / 필터 / 페이지네이션 테이블
static/js/detail.js            CVE 상세 렌더링
data/known_exploited_vulnerabilities.csv  CISA KEV 카탈로그 원본
```

## API

| 엔드포인트 | 설명 |
|---|---|
| `GET /api/summary` | KPI 합계 (전체/벤더/제품/랜섬웨어/평균 대응기간) |
| `GET /api/trends` | 월별 KEV 등록 건수 |
| `GET /api/vendors?limit=10` | 벤더별 CVE 건수 상위 N |
| `GET /api/products?limit=10` | 제품별 CVE 건수 상위 N |
| `GET /api/cwes?limit=10` | CWE별 CVE 건수 상위 N |
| `GET /api/ransomware` | Known / Unknown 랜섬웨어 연관 건수 |
| `GET /api/response-time` | 대응기간(dueDate - dateAdded) 구간별 분포 |
| `GET /api/filters` | 검색 페이지 드롭다운용 벤더/연도 목록 |
| `GET /api/vulnerabilities?keyword=&vendor=&ransomware=&year=` | 검색/필터 |
| `GET /api/vulnerabilities/<cveID>` | CVE 상세 (없으면 404) |
