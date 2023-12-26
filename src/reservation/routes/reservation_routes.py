from uuid import UUID

from flask import Blueprint, request, jsonify, Response

from exceptions import exceptions
from service.reservation_service import ReservationService

reservation_app = Blueprint("reservation", __name__, url_prefix="/reservations")

reservation_service = ReservationService()


@reservation_app.route("/", methods=["POST"])
def create_reservation():
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    book_uid = json_body["bookUid"]
    library_uid = json_body["libraryUid"]
    till_date = json_body["tillDate"]

    result = reservation_service.create_reservation(username, book_uid, library_uid, till_date)
    return jsonify(result.to_dict())


@reservation_app.route("/<reservation_uid>/return", methods=["POST"])
def return_reservation(reservation_uid: UUID):
    json_body = request.get_json()
    date = json_body["date"]

    try:
        reservation_service.close_reservation(reservation_uid, date)
    except exceptions.ReservationNotFound:
        return jsonify({
            "message": "not found"
        }), 404

    return Response(status=204)


@reservation_app.route("/", methods=["GET"])
def get_all_reservations():
    username = request.headers.get("X-User-Name")
    reservations = reservation_service.get_all_reservations(username)
    return jsonify([reservation.to_dict() for reservation in reservations])


@reservation_app.route("/<reservation_uid>/delete", methods=["GET"])
def delete_reservation():
    pass


@reservation_app.route("/rented")
def get_rented_reservations_count():
    username = request.headers.get("X-User-Name")
    count = reservation_service.get_rented_reservations_count(username)
    return jsonify({"count": count})


@reservation_app.route("/<reservation_uid>")
def get_reservation(reservation_uid: UUID):
    reservation = reservation_service.get_reservation(reservation_uid)
    return jsonify(reservation.to_dict())
