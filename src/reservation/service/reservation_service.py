import uuid
from datetime import date
from uuid import UUID

from db.models import db
from db.repositories import ReservationRepository
from domain.entities import Reservation
from domain.entities import ReservationStatus
from dto.api.reservation_dto import ReservationAPI
from dto.api.reservation_dto import ReservationFullAPI
from exceptions import exceptions
from mapper import reservation_mapper


class ReservationService:

    def __init__(self):
        self._reservation_repository = ReservationRepository(db.session)

    def create_reservation(self, username: str, book_uid: UUID, library_uid: UUID, till_date: str) -> ReservationAPI:
        reservation = Reservation(
            id=None,
            reservation_uid=uuid.uuid4(),
            username=username,
            book_uid=book_uid,
            library_uid=library_uid,
            status=ReservationStatus.RENTED,
            start_date=date.today(),
            till_date=date.fromisoformat(till_date),
        )
        reservation = self._reservation_repository.create_reservation(reservation)
        return reservation_mapper.reservation_to_dto(reservation)

    def close_reservation(self, reservation_uid: UUID, return_date: str):
        reservation = self._reservation_repository.get_by_uid(reservation_uid)
        if reservation is None:
            raise exceptions.ReservationNotFound()

        reservation_till_date = reservation.till_date
        current_date = date.fromisoformat(return_date)

        if current_date > reservation_till_date:
            new_status = ReservationStatus.EXPIRED
        else:
            new_status = ReservationStatus.RETURNED

        reservation.status = new_status
        self._reservation_repository.update_reservation(reservation)

    def get_all_reservations(self, username) -> list[ReservationFullAPI]:
        reservations = self._reservation_repository.list_by_username(username)
        return [reservation_mapper.reservation_to_full_dto(reservation) for reservation in reservations]

    def get_rented_reservations_count(self, username: str) -> int:
        reservations = self._reservation_repository.list_rented_by_username(username)
        return len(reservations)

    def get_reservation(self, reservation_uid) -> ReservationFullAPI:
        reservation = self._reservation_repository.get_by_uid(reservation_uid)
        return reservation_mapper.reservation_to_full_dto(reservation)
