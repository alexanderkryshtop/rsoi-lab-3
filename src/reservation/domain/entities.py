from typing import Optional

import enum
from dataclasses import dataclass
from datetime import date
from uuid import UUID


class ReservationStatus(enum.Enum):
    RENTED = "RENTED"
    RETURNED = "RETURNED"
    EXPIRED = "EXPIRED"


@dataclass
class Reservation:
    id: Optional[int]
    reservation_uid: UUID
    username: str
    book_uid: UUID
    library_uid: UUID
    status: ReservationStatus
    start_date: date
    till_date: date
