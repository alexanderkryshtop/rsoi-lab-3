import requests
from flask import Blueprint, request, current_app, Response

library_app = Blueprint("library", __name__, url_prefix="/api/v1/libraries")


@library_app.route("/")
def get_libraries():
    page = request.args.get("page")
    size = request.args.get("size")
    city = request.args.get("city")
    if not city:
        return Response(status=400)

    decoded_query_string = request.query_string.decode()
    prefix = current_app.config['library']

    url = f"{prefix}/libraries?{decoded_query_string}"
    result = requests.get(url)

    return result.text, result.status_code, {"Content-Type": "application/json"}


@library_app.route("/<library_uid>/books")
def get_books_in_library(library_uid: str):
    page = request.args.get("page")
    size = request.args.get("size")
    show_all = request.args.get("showAll")

    decoded_query_string = request.query_string.decode()
    prefix = current_app.config['library']

    url = f"{prefix}/libraries/{library_uid}/books?{decoded_query_string}"
    result = requests.get(url)

    return result.text, result.status_code, {"Content-Type": "application/json"}
