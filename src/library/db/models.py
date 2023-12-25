from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class LibraryModel(db.Model):
    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key=True)
    library_uid = db.Column(db.UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_uid = db.Column(db.UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    condition = db.Column(db.String(255), nullable=False)


class LibraryBooksModel(db.Model):
    __tablename__ = 'library_books'

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), primary_key=True)
    available_count = db.Column(db.Integer)
