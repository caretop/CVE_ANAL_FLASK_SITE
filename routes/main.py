from flask import Blueprint, render_template

from analysis.visualize import example_monthly_trend

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # analysis/visualize.py 의 예시 함수 하나를 실제로 연결해 둔 것입니다.
    # 새 차트를 추가하면 여기서 호출하고 render_template에 넘겨주세요.
    monthly_trend_chart = example_monthly_trend()
    return render_template("index.html", monthly_trend_chart=monthly_trend_chart)


@main_bp.route("/vulnerabilities")
def vulnerabilities():
    return render_template("vulnerabilities.html")


@main_bp.route("/vulnerability/<cve_id>")
def vulnerability_detail(cve_id):
    return render_template("detail.html", cve_id=cve_id)
