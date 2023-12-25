import requests
from flask import Blueprint, request, current_app, jsonify

reservation_app = Blueprint("reservation", __name__, url_prefix="/api/v1/reservations")

from service.reservation_service import ReservationService


@reservation_app.route("/", methods=["POST"])
def take_book_in_library():
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    book_uid = json_body["bookUid"]
    library_uid = json_body["libraryUid"]
    till_date = json_body["tillDate"]

    response, status_code = ReservationService.reservation_process_create(username, book_uid, library_uid, till_date)

    return jsonify(response), status_code


@reservation_app.route("/<reservation_uid>/return", methods=["POST"])
def return_book_to_library(reservation_uid: str):
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    condition = json_body["condition"]
    current_date = json_body["date"]

    response, status_code = ReservationService.reservation_process_return(reservation_uid, username, condition, current_date)
    return jsonify(response), status_code


@reservation_app.route("/", methods=["GET"])
def get_all_reservations():
    username = request.headers.get("X-User-Name")

    response, status_code = ReservationService.get_all_reservations(username)
    return jsonify(response), status_code
