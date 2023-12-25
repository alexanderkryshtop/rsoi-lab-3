from dataclasses import dataclass
from uuid import UUID


@dataclass
class Library:
    id: int
    library_uid: UUID
    name: str
    city: str
    address: str


@dataclass
class Book:
    id: int
    book_uid: UUID
    name: str
    author: str
    genre: str
    condition: str
