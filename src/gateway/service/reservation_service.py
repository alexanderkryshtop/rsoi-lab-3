from datetime import date
from typing import Tuple, Any, Optional

import requests
from flask import current_app
from service.library_service import LibraryService
from service.rating_service import RatingService
from request_queue import Queue

class ReservationService:

    @staticmethod
    def _get_rented_reservations_count(username: str) -> int:
        result = requests.get(
            f"{current_app.config['reservation']}/reservations/rented",
            headers={"X-User-Name": username}
        )
        json_data = result.json()
        return json_data["count"]

    @staticmethod
    def _create_reservation(username: str, book_uid: str, library_uid: str, till_date: str):
        json_body = {
            "bookUid": book_uid,
            "libraryUid": library_uid,
            "tillDate": till_date
        }
        url = f"{current_app.config['reservation']}/reservations"
        result = requests.post(url, json=json_body, headers={"X-User-Name": username})

        json_data = result.json()
        return json_data, result.status_code

    @staticmethod
    def _update_reservation(reservation_uid: str, current_date: str) -> int:
        try:
            json_body = {
                "date": current_date
            }
            url = f"{current_app.config['reservation']}/reservations/{reservation_uid}/return"
            result = requests.post(url, json=json_body)
            return result.status_code
        except Exception:
            return 503

    @staticmethod
    def _get_reservation(reservation_uid: str) -> tuple[Any, int]:
        try:
            url = f"{current_app.config['reservation']}/reservations/{reservation_uid}"
            result = requests.get(url)

            json_data = result.json()
            return json_data, result.status_code
        except Exception:
            return None, 503

    @staticmethod
    def reservation_process_create(username: str, book_uid: str, library_uid: str, till_date: str) -> Tuple[Any, int]:
        rating, status_code = RatingService.get_user_rating(username)
        if status_code != 200:
            return {"message": "Bonus Service unavailable"}, 503

        available_count, status_code = LibraryService.get_book_available_count(book_uid, library_uid)
        if available_count <= 0:
            return {"message": "book is not available"}, 404

        rented_count = ReservationService._get_rented_reservations_count(username)
        if rating <= rented_count:
            return {"message": "not enough stars"}, 200

        reservation, status_code = ReservationService._create_reservation(username, book_uid, library_uid, till_date)
        status_code = LibraryService.checkout_book(book_uid, library_uid)

        book, status_code = LibraryService.get_book(book_uid)
        library, status_code = LibraryService.get_library(library_uid)

        result = {
            "reservationUid": reservation["reservationUid"],
            "status": reservation["status"],
            "startDate": reservation["startDate"],
            "tillDate": reservation["endDate"],
            "book": book,
            "library": library,
            "rating": rating,
        }

        return result, 200

    @staticmethod
    def reservation_process_return(
            reservation_uid: str,
            username: str,
            condition: str,
            current_date: str
    ) -> Tuple[Optional[dict], int]:
        reservation, status_code = ReservationService._get_reservation(reservation_uid)
        if status_code == 503:
            return None, 503

        status_code = ReservationService._update_reservation(reservation_uid, current_date)
        if status_code == 503:
            return None, 503

        book_uid = reservation["bookUid"]
        library_uid = reservation["libraryUid"]
        status_code = LibraryService.return_book(book_uid, library_uid)
        if status_code == 503:
            Queue.enqueue(f"{current_app.config['library']}/libraries/book/return", requests.post, data={
                "bookUid": book_uid, "libraryUid": library_uid,
            })

        book, status_code = LibraryService.get_book(book_uid)

        required_date = date.fromisoformat(reservation["endDate"])
        returning_date = date.fromisoformat(current_date)

        decrease = 0
        increase = 0
        decreased = False
        if book["condition"] != condition:
            decrease += 10
            decreased = True
        if returning_date > required_date:
            decrease += 10
            decreased = True
        if not decreased:
            increase = 1

        _, status_code = RatingService.increase_user_rating(username, increase - decrease)
        if status_code == 503:
            Queue.enqueue(f"{current_app.config['rating']}/rating", requests.get, {"X-User-Name": username})
        return None, 204

    @staticmethod
    def get_all_reservations(username: str) -> Tuple[Any, int]:
        result = requests.get(
            f"{current_app.config['reservation']}/reservations/",
            headers={"X-User-Name": username}
        )
        reservations = result.json()
        res = []

        for reservation in reservations:
            book_uid = reservation["bookUid"]
            library_uid = reservation["libraryUid"]
            book, status_code = LibraryService.get_book(book_uid)
            library, status_code = LibraryService.get_library(library_uid)
            res.append({
                "reservationUid": reservation["reservationUid"],
                "status": reservation["status"],
                "startDate": reservation["startDate"],
                "tillDate": reservation["endDate"],
                "book": book or book_uid,
                "library": library or library_uid
            })

        return res, result.status_code
