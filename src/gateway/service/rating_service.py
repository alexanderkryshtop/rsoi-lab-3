from typing import Tuple
from typing import Any

import requests
from flask import current_app


class RatingService:

    @staticmethod
    def get_user_rating(username: str) -> Tuple[Any, int]:
        try:
            result = requests.get(
                f"{current_app.config['rating']}/rating",
                headers={"X-User-Name": username}
            )
            json_data = result.json()
        except Exception:
            return None, 503
        return json_data["stars"], result.status_code

    @staticmethod
    def update_user_rating(username: str, new_rating: int) -> Tuple[int, int]:
        json_body = {"count": new_rating}
        result = requests.post(
            f"{current_app.config['rating']}/rating/change",
            headers={"X-User-Name": username},
            json=json_body
        )
        json_data = result.json()
        return json_data["stars"], result.status_code
