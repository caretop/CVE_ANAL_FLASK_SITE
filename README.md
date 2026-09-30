# CISA KEV 대시보드 (Flask)

데스크탑(내 컴퓨터)에서 바로 돌리는 단순한 Flask 웹 서버입니다. CISA의
"알려진 악용 취약점(KEV, Known Exploited Vulnerabilities)" 목록을 읽어서,
숫자로 요약하고(KPI), 검색할 수 있게 하고, 원하는 그래프를 얹을 수 있는
자리까지 마련해 둔 프로젝트입니다.

**파이썬을 처음 다뤄보는 분도 따라 할 수 있도록** 이 문서는 설치부터
"내 그래프 하나 추가해보기"까지 전부 순서대로 설명합니다. 막히는 부분이
있으면 맨 아래 [자주 발생하는 오류](#자주-발생하는-오류) 절을 확인하세요.

---

## 목차

1. [이 프로젝트가 하는 일](#1-이-프로젝트가-하는-일)
2. [시작하기 전에 준비할 것](#2-시작하기-전에-준비할-것)
3. [설치하고 실행하기 (단계별)](#3-설치하고-실행하기-단계별)
4. [폴더 구조 한눈에 보기](#4-폴더-구조-한눈에-보기)
5. [데이터는 이렇게 흘러갑니다](#5-데이터는-이렇게-흘러갑니다)
6. [나만의 시각화 추가하기](#6-나만의-시각화-추가하기)
7. [API 목록](#7-api-목록)
8. [데이터 소스: CSV 기본 + MongoDB 폴백](#8-데이터-소스-csv-기본--mongodb-폴백)
9. [자주 발생하는 오류](#9-자주-발생하는-오류)

---

## 1. 이 프로젝트가 하는 일

- `data/known_exploited_vulnerabilities.csv` 파일(CISA의 공식 KEV 카탈로그)을
  읽어서 pandas라는 표 계산 라이브러리로 정리합니다.
- 정리한 데이터를 가지고
  - **대시보드 화면**(`/`)에서 전체 건수 같은 요약 숫자(KPI)를 보여주고,
  - **검색 화면**(`/vulnerabilities`)에서 CVE를 키워드/벤더/랜섬웨어 여부/연도로 찾아보고,
  - **상세 화면**(`/vulnerability/CVE-xxxx-xxxxx`)에서 CVE 하나의 전체 정보를 보여주고,
  - **API**(`/api/...`)로 JSON 형태의 통계 데이터도 제공합니다.
- 대시보드의 차트 영역은 **일부러 비워두거나(빈 틀) 예시 하나만 채워둔 상태**입니다.
  여러분이 원하는 방식(파이썬 matplotlib, plotly, 또는 자바스크립트 차트
  라이브러리 등)으로 자유롭게 채우면 됩니다. → [6번](#6-나만의-시각화-추가하기) 참고.

## 2. 시작하기 전에 준비할 것

- **파이썬 3.9 이상**이 설치되어 있어야 합니다.
  - 설치 여부 확인: 터미널(명령 프롬프트)을 열고 아래 명령을 입력하세요.
    ```bash
    python3 --version
    ```
    `Python 3.9.x` 이상이 나오면 됩니다. 만약 명령을 못 찾는다는 오류가 나오면
    [python.org](https://www.python.org/downloads/)에서 파이썬을 먼저 설치하세요.
    (Windows에서는 `python3` 대신 `python`으로 실행해야 할 수도 있습니다.)
- MongoDB는 **필요하지 않습니다.** 이 프로젝트는 CSV 파일만으로 바로 실행됩니다.
  (MongoDB는 선택 사항입니다. [8번](#8-데이터-소스-csv-기본--mongodb-폴백) 참고)

## 3. 설치하고 실행하기 (단계별)

터미널을 열고, 이 프로젝트 폴더로 이동한 뒤 아래를 순서대로 입력합니다.

**① 가상환경 만들기** (이 프로젝트만을 위한 독립된 파이썬 공간을 만드는 것입니다.
다른 프로젝트와 라이브러리가 섞이지 않도록 해줍니다.)

```bash
python3 -m venv .venv
```

**② 가상환경 켜기(활성화)**

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (명령 프롬프트)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

성공하면 터미널 맨 앞에 `(.venv)`라는 표시가 붙습니다. 이후 명령어는 전부 이
상태(가상환경이 켜진 상태)에서 실행하세요.

**③ 필요한 라이브러리 설치하기**

```bash
pip install -r requirements.txt
```

`requirements.txt`에 적힌 Flask(웹 서버), pandas(데이터 처리), matplotlib
(그래프), pymongo(MongoDB 연결), python-dotenv(설정 파일 읽기)가 한 번에
설치됩니다. 시간이 조금 걸릴 수 있습니다.

**④ 설정 파일 만들기**

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

`.env` 파일은 "환경 설정" 파일입니다. 기본값 그대로 두어도 잘 동작합니다.
(내용은 [8번](#8-데이터-소스-csv-기본--mongodb-폴백)에서 설명합니다.)

**⑤ 서버 실행하기**

```bash
python app.py
```

터미널에 아래와 비슷한 줄이 보이면 성공입니다.

```
 * Running on http://127.0.0.1:5000
```

**⑥ 브라우저로 확인하기**

웹 브라우저를 열고 주소창에 `http://127.0.0.1:5000` 을 입력하세요.
대시보드 화면이 보이면 성공입니다.

서버를 끄고 싶으면 터미널에서 `Ctrl + C`를 누르세요.

> **다음에 다시 실행할 때는** ①③④를 반복할 필요 없이, 프로젝트 폴더에서
> ②(가상환경 켜기) → ⑤(`python app.py`)만 하면 됩니다.

## 4. 폴더 구조 한눈에 보기

```
CVE_ANAL_FLASK_SITE/
├── app.py                     ▶ 서버를 켜는 시작점. python app.py로 실행합니다.
├── config.py                  ▶ 설정값(.env 파일 읽기)
├── requirements.txt           ▶ 설치해야 할 라이브러리 목록
├── .env.example                ▶ 설정 파일 예시 (복사해서 .env로 사용)
│
├── data/
│   └── known_exploited_vulnerabilities.csv   ▶ CISA KEV 원본 데이터
│
├── analysis/
│   ├── kev_analysis.py        ▶ 데이터를 읽고 집계(통계)하는 함수들
│   └── visualize.py           ★ 여기에 여러분의 그래프 함수를 추가하세요
│
├── routes/
│   ├── main.py                ▶ 화면(HTML 페이지) 라우트 (/, /vulnerabilities, ...)
│   └── api.py                 ▶ JSON API 라우트 (/api/...)
│
├── templates/                 ▶ 화면의 뼈대(HTML). Jinja2라는 문법을 사용합니다.
│   ├── base.html               (공통 레이아웃: 상단 메뉴 등)
│   ├── index.html               ★ 대시보드 화면 (차트를 배치하는 곳)
│   ├── vulnerabilities.html     검색 화면
│   └── detail.html              CVE 상세 화면
│
├── static/
│   ├── css/style.css          ▶ 디자인(색상, 여백 등)
│   └── js/                    ▶ 검색/필터 등의 동작(자바스크립트)
│
└── scripts/
    └── import_to_mongo.py     ▶ CSV를 MongoDB로 옮기는 도구 (선택 사항)
```

★ 표시된 두 파일(`analysis/visualize.py`, `templates/index.html`)이 시각화를
추가할 때 주로 건드리게 될 파일입니다.

## 5. 데이터는 이렇게 흘러갑니다

```
CSV 파일 (또는 MongoDB)
     │  pandas로 읽어들임
     ▼
analysis/kev_analysis.py
     │  · 날짜 계산 (대응기간 = 조치기한 - 등록일)
     │  · 통계 함수 (get_summary, get_trends, get_vendor_stats, get_cwe_stats, ...)
     ▼
   ┌──────────────┬───────────────────────┐
   │              │                       │
routes/api.py   routes/main.py      analysis/visualize.py
(JSON 응답)      (HTML 화면 렌더링)     (그래프 이미지 생성)
   │              │                       │
   ▼              ▼                       ▼
/api/... 로     화면(.html)에         화면에 <img>로 바로 삽입
JSON 데이터      데이터를 채워 표시
제공
```

핵심은 **데이터를 만드는 부분(`kev_analysis.py`)과 보여주는 부분(화면, API)이
분리**되어 있다는 것입니다. 어떤 통계가 필요하면 `kev_analysis.py`에 함수를
하나 추가하면, 화면에서도 API에서도 똑같이 가져다 쓸 수 있습니다.

## 6. 나만의 시각화 추가하기

대시보드(`/`)를 열어보면 차트 자리가 6개 있습니다. 첫 번째("월별 KEV 등록
추이")는 이미 실제로 동작하는 예시로 채워져 있고, 나머지 5개는 아직 빈
틀(점선 박스)입니다. 이 절에서는 **파이썬(matplotlib)으로 빈 틀 하나를 실제
그래프로 채우는 과정을 처음부터 끝까지** 따라 해봅니다.

예시로 "벤더별 KEV" 차트를 막대그래프로 채워보겠습니다.

### 1단계. 어떤 데이터가 있는지 확인하기

`analysis/kev_analysis.py`를 열어보면 `get_vendor_stats(limit=None)` 함수가
있습니다. 이 함수는 아래처럼 생긴 리스트를 돌려줍니다.

```python
[{"vendor": "Microsoft", "count": 389}, {"vendor": "Cisco", "count": 99}, ...]
```

(같은 데이터를 브라우저에서 직접 보고 싶다면 서버를 켠 상태에서
`http://127.0.0.1:5000/api/vendors?limit=10` 주소로 들어가면 JSON으로
보입니다.)

### 2단계. `analysis/visualize.py`에 함수 추가하기

이 파일 맨 아래 주석 처리된 틀을 참고해서, 아래 함수를 **주석이 아닌 실제
코드로** 추가합니다.

```python
from analysis.kev_analysis import get_vendor_stats  # 파일 위쪽 import 부분에 추가

def example_top_vendors():
    data = get_vendor_stats(limit=10)
    vendors = [row["vendor"] for row in data]
    counts = [row["count"] for row in data]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(vendors, counts)      # barh = 가로 막대그래프
    ax.invert_yaxis()             # 건수가 가장 많은 벤더가 위로 오도록 뒤집기
    ax.set_title("벤더별 KEV 건수 Top 10")
    fig.tight_layout()

    return fig_to_base64(fig)     # 이 한 줄이 그래프를 이미지로 바꿔줍니다
```

### 3단계. `routes/main.py`에서 함수 연결하기

```python
from analysis.visualize import example_monthly_trend, example_top_vendors  # 추가

@main_bp.route("/")
def index():
    monthly_trend_chart = example_monthly_trend()
    top_vendors_chart = example_top_vendors()  # 추가
    return render_template(
        "index.html",
        monthly_trend_chart=monthly_trend_chart,
        top_vendors_chart=top_vendors_chart,   # 추가
    )
```

### 4단계. `templates/index.html`에서 빈 틀을 이미지로 바꾸기

"벤더별 KEV" 카드를 찾아서, `<div class="chart-placeholder" ...>...</div>`
부분을 아래처럼 바꿉니다.

```html
<div class="chart-card">
  <h2>벤더별 KEV</h2>
  <img class="chart-image" src="data:image/png;base64,{{ top_vendors_chart }}"
       alt="벤더별 KEV 막대그래프">
</div>
```

### 5단계. 저장하고 서버 재시작 후 확인

파일을 저장한 뒤, 터미널에서 서버를 껐다가(`Ctrl+C`) 다시 켭니다
(`python app.py`). 브라우저에서 새로고침하면 새 그래프가 보입니다.

> Flask 개발 서버는 코드가 바뀌어도 자동으로 반영되지 않습니다(이 프로젝트는
> 일부러 가장 단순한 기본 설정을 사용합니다). 코드를 고칠 때마다 서버를
> 껐다 켜야 결과가 반영됩니다.

### 이 패턴을 복사해서 나머지 차트도 채우기

나머지 빈 틀(랜섬웨어 연관 여부, 제품별 KEV, CWE 분포, 대응기간 분포)도
같은 3단계(① `visualize.py`에 함수 추가 → ② `main.py`에서 연결 → ③
`index.html`에서 표시)를 반복하면 됩니다. 사용할 데이터 함수는 카드 밑의
점선 박스에 적힌 API 경로와 같은 이름입니다.

| 차트 | 데이터 함수 (`analysis/kev_analysis.py`) | 참고 API |
|---|---|---|
| 벤더별 KEV | `get_vendor_stats(limit=10)` | `GET /api/vendors` |
| 랜섬웨어 연관 여부 | `get_ransomware_stats()` | `GET /api/ransomware` |
| 제품별 KEV | `get_product_stats(limit=10)` | `GET /api/products` |
| CWE 분포 | `get_cwe_stats(limit=10)` | `GET /api/cwes` |
| 대응기간 분포 | `get_response_time_stats()` | `GET /api/response-time` |

### matplotlib 대신 다른 방식을 쓰고 싶다면?

- **plotly** 같은 라이브러리로 인터랙티브(마우스로 확대/축소되는) 차트를
  만들고 싶다면, `pip install plotly`로 설치한 뒤 `fig.to_html()`로 HTML
  문자열을 만들어서 템플릿에 `{{ 차트변수 | safe }}`로 넣으면 됩니다.
- **자바스크립트**(Chart.js, D3, ECharts 등)로 그리고 싶다면
  `analysis/visualize.py`는 건드릴 필요 없이, `/api/vendors`처럼 이미
  제공되는 JSON API를 `static/js/dashboard.js`에서 `fetch()`로 불러와
  그리면 됩니다. (이전 버전에서 실제로 이렇게 구현했던 예시가 git 이력에
  남아 있으니 참고할 수 있습니다.)
- 꼭 "그래프"가 아니어도 됩니다. 표(HTML 테이블)나 간단한 텍스트 요약을
  돌려줘도 됩니다 — 템플릿에서 그 값을 그대로 출력하면 "결과 전달"이 됩니다.

## 7. API 목록

브라우저 주소창에 아래 경로를 직접 입력해서 JSON 결과를 바로 볼 수 있습니다.

| 엔드포인트 | 설명 |
|---|---|
| `GET /api/summary` | KPI 합계 (전체/벤더/제품/랜섬웨어/평균 대응기간) |
| `GET /api/trends` | 월별 KEV 등록 건수 |
| `GET /api/vendors?limit=10` | 벤더별 CVE 건수 상위 N |
| `GET /api/products?limit=10` | 제품별 CVE 건수 상위 N |
| `GET /api/cwes?limit=10` | CWE별 CVE 건수 상위 N |
| `GET /api/ransomware` | Known / Unknown 랜섬웨어 연관 건수 |
| `GET /api/response-time` | 대응기간(dueDate - dateAdded) 구간별 분포 |
| `GET /api/filters` | 검색 화면 드롭다운용 벤더/연도 목록 |
| `GET /api/vulnerabilities?keyword=&vendor=&ransomware=&year=` | 검색/필터 |
| `GET /api/vulnerabilities/<cveID>` | CVE 상세 (없으면 404) |

## 8. 데이터 소스: CSV 기본 + MongoDB 폴백

`.env` 파일의 `DATA_SOURCE` 값으로 제어합니다.

- `csv` (기본값) — `data/known_exploited_vulnerabilities.csv`에서 읽습니다.
  **파일이 없거나 비어 있으면 자동으로 MongoDB로 전환(폴백)**됩니다.
- `mongo` — MongoDB만 사용하도록 강제합니다.

MongoDB를 함께 쓰고 싶다면(선택 사항), 로컬에 MongoDB를 설치/실행한 뒤 아래
명령으로 CSV 내용을 한 번 옮겨두면 됩니다.

```bash
python scripts/import_to_mongo.py
```

이후 `.env`의 `MONGO_URI` / `MONGO_DB` / `MONGO_COLLECTION` 값으로 접속
정보를 바꿀 수 있습니다. 어떤 소스를 쓰든 `analysis/kev_analysis.py`가 같은
형태의 데이터로 만들어주기 때문에, 화면과 API 동작은 완전히 동일합니다.

## 9. 자주 발생하는 오류

| 증상 | 원인 / 해결 방법 |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` 등 | 가상환경을 켜지 않았거나(`source .venv/bin/activate`), `pip install -r requirements.txt`를 안 했을 가능성이 큽니다. |
| `command not found: python3` (Windows) | Windows에서는 `python`을 대신 사용해보세요. |
| `Address already in use` / 포트 5000 관련 오류 | 이미 서버가 켜져 있거나 다른 프로그램이 5000번 포트를 쓰고 있습니다. 기존 서버를 끄거나(`Ctrl+C`), `app.py` 맨 아래 `port=5000`을 다른 숫자(예: 5050)로 바꾸세요. |
| 그래프의 한글이 네모 박스(□)로 보임 | 한글 폰트가 없는 리눅스 환경일 수 있습니다. `sudo apt-get install fonts-nanum` 설치 후 서버를 재시작하세요. (Windows/Mac은 보통 문제 없습니다.) |
| `FileNotFoundError: KEV CSV file not found` | `data/known_exploited_vulnerabilities.csv` 파일이 삭제되었거나 경로가 바뀌었습니다. 파일이 있는지 확인하거나 `.env`의 `KEV_CSV_PATH`를 확인하세요. |
| 코드를 고쳤는데 화면이 그대로임 | Flask 개발 서버를 껐다(`Ctrl+C`) 다시 켜야(`python app.py`) 반영됩니다. |
| `pip install`이 너무 오래 걸리거나 실패함 | 인터넷 연결을 확인하세요. 사내망/방화벽 환경이라면 관리자에게 문의가 필요할 수 있습니다. |
