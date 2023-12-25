from flask import Blueprint
from flask import Response

gateway_app = Blueprint("gateway", __name__, url_prefix="/")


@gateway_app.route("/manage/health")
def healthcheck():
    return Response(status=200)
