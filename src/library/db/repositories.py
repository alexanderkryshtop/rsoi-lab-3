from typing import Optional
from uuid import UUID

from db.models import LibraryModel, BookModel, LibraryBooksModel
from domain.entities import Library, Book
from dto.repository.book_dto import BookWithCountRepository
from exceptions import exceptions


class LibraryRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_library_by_uid(self, library_uid: UUID) -> Optional[Library]:
        library_model = self.db_session.query(LibraryModel).filter(LibraryModel.library_uid == library_uid).first()
        return self._to_entity(library_model) if library_model else None

    def get_libraries_by_city(self, city: str) -> list[Library]:
        library_models = LibraryModel.query.filter_by(city=city).all()
        return [self._to_entity(model) for model in library_models]

    @staticmethod
    def _to_entity(model: LibraryModel):
        return Library(
            id=model.id,
            library_uid=model.library_uid,
            name=model.name,
            city=model.city,
            address=model.address,
        )


class BookRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    def get_book_by_uid(self, book_uid: UUID) -> Optional[Book]:
        book_model = self.db_session.query(BookModel).filter(BookModel.book_uid == book_uid).first()
        return self._to_entity(book_model) if book_model else None

    def get_book_available_count(self, book_uid: UUID, library_uid: UUID) -> int:
        available_count = self.db_session.query(
            LibraryBooksModel.available_count
        ).join(
            BookModel, LibraryBooksModel.book_id == BookModel.id
        ).join(
            LibraryModel, LibraryBooksModel.library_id == LibraryModel.id
        ).filter(
            BookModel.book_uid == book_uid,
            LibraryModel.library_uid == library_uid
        ).scalar()

        return available_count if available_count is not None else 0

    def find_books_by_library_uid(self, library_uid: UUID) -> list[BookWithCountRepository]:
        book_with_available_counts = self.db_session.query(
            BookModel,
            LibraryBooksModel.available_count
        ).join(
            LibraryBooksModel,
            BookModel.id == LibraryBooksModel.book_id
        ).join(
            LibraryModel,
            LibraryBooksModel.library_id == LibraryModel.id
        ).filter(
            LibraryModel.library_uid == library_uid
        ).all()

        books_with_count = []

        for book_model, available_count in book_with_available_counts:
            book = self._to_entity(book_model)
            book_with_count = BookWithCountRepository(book, available_count)
            books_with_count.append(book_with_count)

        return books_with_count

    def checkout_book(self, library_uid: UUID, book_uid: UUID):
        library = self.db_session.query(LibraryModel).filter_by(library_uid=library_uid).first()
        if not library:
            raise exceptions.LibraryNotFound()

        library_book = self.db_session.query(LibraryBooksModel).join(BookModel).filter(
            LibraryBooksModel.library_id == library.id,
            BookModel.book_uid == book_uid
        ).first()
        if not library_book:
            raise exceptions.BookNotFoundInLibrary()

        if library_book.available_count < 1:
            raise exceptions.BookNotAvailable()

        library_book.available_count -= 1
        self.db_session.commit()

    def return_book(self, library_uid: UUID, book_uid: UUID):
        library = self.db_session.query(LibraryModel).filter_by(library_uid=library_uid).first()
        if not library:
            raise exceptions.LibraryNotFound()

        library_book = self.db_session.query(LibraryBooksModel).join(BookModel).filter(
            LibraryBooksModel.library_id == library.id,
            BookModel.book_uid == book_uid
        ).first()
        if not library_book:
            raise exceptions.BookNotFoundInLibrary()

        library_book.available_count += 1
        self.db_session.commit()

    @staticmethod
    def _to_entity(model: BookModel):
        return Book(
            id=model.id,
            book_uid=model.book_uid,
            name=model.name,
            author=model.author,
            genre=model.genre,
            condition=model.condition,
        )
