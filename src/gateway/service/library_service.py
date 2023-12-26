from typing import Tuple
from typing import Any
from typing import Optional

import requests
from flask import current_app


class LibraryService:

    @staticmethod
    def get_book_available_count(book_uid: str, library_uid: str) -> Tuple[int, int]:
        json_body = {
            "bookUid": book_uid,
            "libraryUid": library_uid,
        }
        result = requests.post(
            f"{current_app.config['library']}/libraries/book/count",
            json=json_body
        )
        json_data = result.json()
        return json_data["count"], result.status_code

    @staticmethod
    def checkout_book(book_uid: str, library_uid: str) -> int:
        json_body = {
            "bookUid": book_uid,
            "libraryUid": library_uid,
        }
        result = requests.post(
            f"{current_app.config['library']}/libraries/book/checkout",
            json=json_body
        )
        return result.status_code

    @staticmethod
    def return_book(book_uid: str, library_uid: str) -> int:
        json_body = {
            "bookUid": book_uid,
            "libraryUid": library_uid,
        }
        result = requests.post(
            f"{current_app.config['library']}/libraries/book/return",
            json=json_body
        )
        return result.status_code

    @staticmethod
    def get_book(book_uid: str) -> Tuple[Any, int]:
        try:
            result = requests.get(
                f"{current_app.config['library']}/libraries/book/{book_uid}",
            )
        except Exception:
            return None, 500
        return result.json(), result.status_code

    @staticmethod
    def get_library(library_uid: str) -> Tuple[Any, int]:
        try:
            result = requests.get(
                f"{current_app.config['library']}/libraries/{library_uid}",
            )
        except Exception:
            return None, 500
        return result.json(), result.status_code
