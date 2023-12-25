from domain.entities import Reservation
from dto.api.reservation_dto import ReservationAPI
from dto.api.reservation_dto import ReservationFullAPI


def reservation_to_dto(reservation: Reservation) -> ReservationAPI:
    return ReservationAPI(
        reservation_uid=reservation.reservation_uid,
        status=reservation.status.value,
        start_date=reservation.start_date,
        till_date=reservation.till_date,
    )


def reservation_to_full_dto(reservation: Reservation) -> ReservationFullAPI:
    return ReservationFullAPI(
        reservation_uid=reservation.reservation_uid,
        status=reservation.status.value,
        start_date=reservation.start_date,
        till_date=reservation.till_date,
        book_uid=reservation.book_uid,
        library_uid=reservation.library_uid,
    )
