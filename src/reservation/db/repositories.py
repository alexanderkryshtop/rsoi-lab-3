from typing import Optional
from uuid import UUID

from db.models import ReservationModel
from db.models import ReservationModelStatus
from domain.entities import Reservation
from exceptions import exceptions


class ReservationRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_reservation(self, reservation: Reservation) -> Reservation:
        reservation_model = self._from_entity(reservation)
        self.db_session.add(reservation_model)
        self.db_session.commit()
        reservation.id = reservation_model.id
        return reservation

    def list_by_username(self, username: str) -> list[Reservation]:
        reservation_models = self.db_session.query(ReservationModel).filter(
            ReservationModel.username == username).all()
        return [self._to_entity(reservation) for reservation in reservation_models]

    def list_rented_by_username(self, username: str) -> list[Reservation]:
        reservation_models = self.db_session.query(ReservationModel).filter(
            ReservationModel.username == username, ReservationModel.status == ReservationModelStatus.RENTED
        ).all()
        return [self._to_entity(reservation) for reservation in reservation_models]

    def get_by_uid(self, reservation_uid: UUID) -> Optional[Reservation]:
        reservation_model = self.db_session.query(ReservationModel).filter(
            ReservationModel.reservation_uid == reservation_uid
        ).one_or_none()
        if not reservation_model:
            return None
        return self._to_entity(reservation_model)

    def update_reservation(self, reservation: Reservation):
        reservation_model = self.db_session.query(ReservationModel).filter(
            ReservationModel.reservation_uid == reservation.reservation_uid
        ).one_or_none()

        if reservation_model is None:
            raise exceptions.ReservationNotFound()

        reservation_model.username = reservation.username
        reservation_model.book_uid = reservation.book_uid
        reservation_model.library_uid = reservation.library_uid
        reservation_model.status = ReservationModelStatus(reservation.status.value)
        reservation_model.start_date = reservation.start_date
        reservation_model.till_date = reservation.till_date

        self.db_session.commit()

    @staticmethod
    def _from_entity(entity: Reservation) -> ReservationModel:
        return ReservationModel(
            reservation_uid=entity.reservation_uid,
            username=entity.username,
            book_uid=entity.book_uid,
            library_uid=entity.library_uid,
            status=ReservationModelStatus(entity.status.value),
            start_date=entity.start_date,
            till_date=entity.till_date,
        )

    @staticmethod
    def _to_entity(model: ReservationModel) -> Reservation:
        return Reservation(
            id=model.id,
            reservation_uid=model.reservation_uid,
            username=model.username,
            book_uid=model.book_uid,
            library_uid=model.library_uid,
            status=model.status,
            start_date=model.start_date.date(),
            till_date=model.till_date.date(),
        )
