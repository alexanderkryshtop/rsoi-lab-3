from flask import Blueprint

healthcheck_app = Blueprint("healthcheck", __name__, url_prefix="/")


@healthcheck_app.route("/manage/health")
def get_libraries():
    return "", 200
