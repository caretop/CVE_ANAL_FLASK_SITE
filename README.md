# CISA KEV Dashboard (Flask)

데스크탑에서 바로 돌리는 단순한 Flask 서버입니다. CISA Known Exploited Vulnerabilities
(KEV) 카탈로그를 pandas로 가공해 KPI/집계/검색 JSON API로 제공하고, 대시보드/검색
목록/CVE 상세 페이지를 렌더링합니다.

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

## 새 차트나 이미지 추가하기

### 방법 1: 파이썬으로 차트 추가하기

이 프로젝트에는 `matplotlib`으로 차트를 만들고 웹페이지에 보여주는 예제가 있습니다. 새 차트도 같은 순서로 추가하면 됩니다.

1. `analysis/visualize.py`에 차트 함수를 만듭니다.

   예를 들어 벤더별 취약점 상위 10개를 막대 그래프로 만들려면, 파일 아래쪽에 다음 함수를 추가합니다.

   ```python
   from analysis.kev_analysis import get_vendor_stats

   def top_vendors_chart():
       data = get_vendor_stats(limit=10)
       vendors = [row["vendor"] for row in data]
       counts = [row["count"] for row in data]

       fig, ax = plt.subplots(figsize=(8, 5))
       ax.barh(vendors, counts)
       ax.invert_yaxis()
       ax.set_title("벤더별 KEV 건수 Top 10")
       fig.tight_layout()

       return fig_to_base64(fig)
   ```

   `get_vendor_stats()`는 벤더 이름과 건수를 가져옵니다. `ax.barh()`가 막대 그래프를 그리고, `fig_to_base64()`가 그래프를 웹페이지에 넣을 수 있는 이미지 데이터로 바꿉니다.

2. `main.py`에서 함수를 가져오고, 대시보드 페이지를 만들 때 호출합니다.

   ```python
   from analysis.visualize import example_monthly_trend, top_vendors_chart
   ```

   기존 `index()` 함수 안에서 차트를 만들고 템플릿에 전달합니다.

   ```python
   def index():
       monthly_trend_chart = example_monthly_trend()
       vendors_chart = top_vendors_chart()
       return render_template(
           "index.html",
           monthly_trend_chart=monthly_trend_chart,
           vendors_chart=vendors_chart,
       )
   ```

3. `index.html`에서 전달받은 차트를 표시합니다.

   ```html
   <img
     src="data:image/png;base64,{{ vendors_chart }}"
     alt="벤더별 KEV 건수 그래프"
   >
   ```

   `vendors_chart`라는 이름은 `main.py`에서 템플릿에 전달한 이름과 같아야 합니다.

4. Flask 서버를 실행하고 대시보드에서 그래프가 보이는지 확인합니다.

   ```bash
   python app.py
   ```

   이미 있는 월별 그래프도 같은 방식으로 만들어집니다. `visualize.py`의 `example_monthly_trend()`가 그래프를 만들고, `main.py`가 템플릿에 전달하며, `index.html`이 화면에 표시합니다.

### 방법 2: JavaScript 차트 추가하기

브라우저에서 차트를 그리려면 다음 순서로 작업합니다.

1. `index.html`에서 원하는 `.chart-placeholder` 영역을 `<canvas>`로 바꿉니다.
2. `dashboard.js`에서 `/api/trends`, `/api/vendors` 같은 API 주소에 요청해 데이터를 가져옵니다.
3. 가져온 데이터를 차트 라이브러리에 전달해 `<canvas>`에 그립니다.

이 방식은 차트 라이브러리 설정이 추가로 필요합니다. 처음 시작한다면 방법 1의 파이썬 차트부터 따라 해보세요. 차트에 필요한 데이터는 이미 `/api/...` API에서 제공됩니다.

### 방법 3: 이미지 파일 추가하기

사진이나 미리 만들어 둔 이미지 파일은 파이썬 코드 없이 넣을 수 있습니다.

1. `static` 폴더 안에 `images` 폴더를 만들고 이미지 파일을 넣습니다.

   ```text
   static/
     images/
       example.png
   ```

2. 표시할 템플릿 파일에 이미지 태그를 추가합니다.

   ```html
   <img
     src="{{ url_for('static', filename='images/example.png') }}"
     alt="이미지 설명"
   >
   ```

3. Flask 서버를 실행하고 해당 페이지에서 이미지가 보이는지 확인합니다.

`static`은 브라우저에 제공하는 파일을 두는 폴더입니다. 이미지 파일은 `static/images/`에, 페이지 HTML은 `templates`에 둡니다.


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
