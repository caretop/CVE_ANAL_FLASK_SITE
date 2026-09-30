from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/vulnerabilities")
def vulnerabilities():
    return render_template("vulnerabilities.html")


@main_bp.route("/vulnerability/<cve_id>")
def vulnerability_detail(cve_id):
    return render_template("detail.html", cve_id=cve_id)
