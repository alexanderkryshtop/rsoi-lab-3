from typing import Optional
from uuid import UUID

from db.models import db
from db.repositories import BookRepository
from db.repositories import LibraryRepository
from dto.api.book_dto import BookAPI
from dto.api.book_dto import BookWithCountAPI
from dto.api.library_dto import LibraryAPI
from mapper import book_mapper
from mapper import library_mapper


class LibraryService:

    def __init__(self):
        self._library_repository = LibraryRepository(db.session)
        self._book_repository = BookRepository(db.session)

    def get_libraries(self, city: str) -> list[LibraryAPI]:
        libraries = self._library_repository.get_libraries_by_city(city)
        return [library_mapper.library_to_dto(library) for library in libraries]

    def get_books_in_library(self, library_uid: UUID) -> list[BookWithCountAPI]:
        books_with_available_count = self._book_repository.find_books_by_library_uid(library_uid)
        return [book_mapper.repository_to_api(book) for book in books_with_available_count]

    def checkout_book(self, book_uid: UUID, library_uid: UUID):
        self._book_repository.checkout_book(library_uid, book_uid)

    def return_book(self, book_uid: UUID, library_uid: UUID):
        self._book_repository.return_book(library_uid, book_uid)

    def get_book(self, book_uid: UUID) -> Optional[BookAPI]:
        book = self._book_repository.get_book_by_uid(book_uid)
        if not book:
            return None
        return book_mapper.entity_to_api(book)

    def get_book_available_count(self, book_uid: UUID, library_uid: UUID) -> int:
        return self._book_repository.get_book_available_count(book_uid, library_uid)

    def get_library(self, library_uid: UUID) -> Optional[LibraryAPI]:
        library = self._library_repository.get_library_by_uid(library_uid)
        if not library:
            return None
        return library_mapper.library_to_dto(library)
