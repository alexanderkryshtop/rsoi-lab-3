import enum
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReservationModelStatus(enum.Enum):
    RENTED = 'RENTED'
    RETURNED = 'RETURNED'
    EXPIRED = 'EXPIRED'


class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    reservation_uid = db.Column(db.UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    username = db.Column(db.String(80), nullable=False)
    book_uid = db.Column(db.UUID(as_uuid=True), nullable=False, default=uuid4)
    library_uid = db.Column(db.UUID(as_uuid=True), nullable=False, default=uuid4)
    status = db.Column(db.Enum(ReservationModelStatus), nullable=False)
    start_date = db.Column(db.TIMESTAMP, nullable=False)
    till_date = db.Column(db.TIMESTAMP, nullable=False)
