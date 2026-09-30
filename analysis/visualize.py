"""시각화를 추가하는 곳입니다.

파이썬 초보자를 위한 가이드는 README.md의 "나만의 시각화 추가하기" 절을
참고하세요. 여기서는 핵심만 짧게 설명합니다.

사용 방법
---------
1. 이 파일에 함수를 하나 만듭니다. 함수 안에서는 analysis.kev_analysis에 있는
   함수(get_dataframe, get_trends, get_vendor_stats, get_cwe_stats, ...)로
   데이터를 가져와 원하는 대로 그래프를 그리면 됩니다.
2. matplotlib으로 그렸다면 마지막에 fig_to_base64(fig)로 변환해서 반환하세요.
   반환한 문자열을 템플릿에서
       <img src="data:image/png;base64,{{ 결과 }}">
   처럼 쓰면 그래프가 그대로 화면에 나타납니다.
3. 꼭 matplotlib일 필요는 없습니다. plotly의 HTML, 표(HTML 문자열), 그냥
   텍스트 요약 등 "결과"라고 부를 수 있는 것이면 무엇이든 함수가 반환하고,
   템플릿에서 그 값을 그대로 출력하면 됩니다.
4. 함수를 만들었으면 routes/main.py의 index()에서 호출해 템플릿으로
   넘겨주고, templates/index.html의 해당 placeholder를 결과로 바꿔주세요.
   (아래 example_monthly_trend()가 실제로 연결되어 있는 예시입니다.)

REST API로 시각화하고 싶다면?
-----------------------------
자바스크립트(Chart.js, D3, ECharts 등)로 그리고 싶다면 이 파일을 쓰지 않아도
됩니다. routes/api.py의 /api/trends, /api/vendors, /api/products, /api/cwes,
/api/ransomware, /api/response-time 이 이미 JSON으로 같은 데이터를 제공합니다.
"""
import base64
import io

import matplotlib

matplotlib.use("Agg")  # 화면(디스플레이) 없는 서버에서도 그래프를 그리기 위한 설정
import matplotlib.pyplot as plt
from matplotlib import font_manager

from analysis.kev_analysis import get_trends

# 한글이 깨지지 않도록(네모 박스로 나오지 않도록) 시스템에 설치된 한글 폰트를
# 자동으로 찾아 씁니다. Windows/Mac은 보통 기본 폰트가 이미 한글을 지원해서
# 여기서 바로 찾힙니다. 한글 폰트가 하나도 없는 리눅스라면 아래처럼
# 설치해 주세요: sudo apt-get install fonts-nanum
_KOREAN_FONT_CANDIDATES = [
    "Malgun Gothic",       # Windows 기본
    "AppleGothic",         # macOS 기본
    "Apple SD Gothic Neo", # macOS(최신)
    "NanumGothic",         # Linux (fonts-nanum)
    "Noto Sans CJK KR",
    "Noto Sans KR",
]


def _use_korean_font():
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _KOREAN_FONT_CANDIDATES:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    else:
        print(
            "[visualize] 한글 폰트를 찾지 못했습니다. 그래프의 한글이 네모 박스로 "
            "보일 수 있습니다. (리눅스라면: sudo apt-get install fonts-nanum)"
        )
    plt.rcParams["axes.unicode_minus"] = False  # 한글 폰트 사용 시 '-' 기호 깨짐 방지


_use_korean_font()


def fig_to_base64(fig):
    """matplotlib figure를 <img> 태그에 바로 쓸 수 있는 base64 문자열로 바꿉니다.

    사용 예:
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        return fig_to_base64(fig)
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)  # 메모리 누수를 막기 위해 그린 뒤에는 꼭 닫아줍니다.
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def example_monthly_trend():
    """예시: 월별 KEV 등록 추이를 선 그래프로 그립니다.

    이 함수를 그대로 복사한 뒤 get_trends() 대신 get_vendor_stats(),
    get_cwe_stats(), get_ransomware_stats() 등을 넣으면 다른 차트도
    같은 방식으로 만들 수 있습니다. (모든 통계 함수는 analysis/kev_analysis.py
    에 있습니다.)
    """
    data = get_trends()  # [{"month": "2021-11", "count": 291}, ...]
    months = [row["month"] for row in data]
    counts = [row["count"] for row in data]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(months, counts, marker="o", markersize=3, linewidth=1.5)
    ax.set_title("월별 KEV 등록 추이")
    ax.set_xlabel("등록 월")
    ax.set_ylabel("건수")
    ax.tick_params(axis="x", rotation=90, labelsize=7)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    return fig_to_base64(fig)


# ---------------------------------------------------------------------------
# 여기부터는 여러분의 차트를 추가하는 자리입니다. 아래는 시작할 때 참고할 수
# 있는 틀(템플릿)입니다. 주석을 해제하고 내용을 채우면 바로 동작합니다.
# ---------------------------------------------------------------------------
#
# from analysis.kev_analysis import get_vendor_stats
#
# def example_top_vendors():
#     data = get_vendor_stats(limit=10)  # [{"vendor": "Microsoft", "count": 389}, ...]
#     vendors = [row["vendor"] for row in data]
#     counts = [row["count"] for row in data]
#
#     fig, ax = plt.subplots(figsize=(8, 5))
#     ax.barh(vendors, counts)
#     ax.invert_yaxis()  # 가장 많은 벤더가 위로 오도록
#     ax.set_title("벤더별 KEV 건수 Top 10")
#     fig.tight_layout()
#
#     return fig_to_base64(fig)
