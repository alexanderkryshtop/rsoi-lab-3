from dataclasses import dataclass
from uuid import UUID


@dataclass
class BookWithCountAPI:
    book_uid: UUID
    name: str
    author: str
    genre: str
    condition: str
    available_count: int

    def to_dict(self) -> dict:
        return {
            "bookUid": self.book_uid,
            "name": self.name,
            "author": self.author,
            "genre": self.genre,
            "condition": self.condition,
            "availableCount": self.available_count,
        }


@dataclass
class BookAPI:
    bookUid: UUID
    author: str
    name: str
    genre: str
    condition: str

    def to_dict(self) -> dict:
        return {
            "bookUid": self.bookUid,
            "author": self.author,
            "name": self.name,
            "genre": self.genre,
            "condition": self.condition,
        }


@dataclass
class BookCheckoutRequestAPI:
    book_uid: UUID
    library_uid: UUID
