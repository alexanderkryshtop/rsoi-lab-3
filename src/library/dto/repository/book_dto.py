from dataclasses import dataclass

from domain.entities import Book


@dataclass
class BookWithCountRepository:
    book: Book
    available_count: int
