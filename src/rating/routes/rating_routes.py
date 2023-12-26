from flask import Blueprint, request

from service.rating_service import RatingService

rating_app = Blueprint("rating", __name__, url_prefix="/rating")

rating_service = RatingService()


@rating_app.route("/")
def get_rating():
    username = request.headers.get("X-User-Name")
    user_stars_count = rating_service.get_star_count(username)

    response = {
        "stars": user_stars_count
    }

    return response, 200


@rating_app.route("/change", methods=["POST"])
def change_rating():
    username = request.headers.get("X-User-Name")

    json_body = request.get_json()
    count = json_body["count"]

    user_stars_count = rating_service.change_star_count(username, count)
    response = {
        "stars": user_stars_count
    }

    return response, 200


@rating_app.route("/increase", methods=["POST"])
def increase_rating():
    username = request.headers.get("X-User-Name")

    json_body = request.get_json()
    count = json_body["count"]

    user_stars_count = rating_service.change_star_count(username, count)
    response = {"stars": user_stars_count}
    return response, 200
