from typing import Optional

from repository import RatingModel


class RatingService:

    def get_star_count(self, username: str) -> Optional[int]:
        ratingModel: RatingModel = RatingModel.query.filter(RatingModel.username == username).one_or_none()
        if not ratingModel:
            ratingModel = RatingModel(username=username, stars=1)
            RatingModel.query.session.add(ratingModel)
            RatingModel.query.session.commit()
        return ratingModel.stars

    def change_star_count(self, username: str, new_count: int) -> Optional[int]:
        ratingModel: RatingModel = RatingModel.query.filter(RatingModel.username == username).one_or_none()
        if not ratingModel:
            return None
        new_rating = new_count
        if new_rating >= 100:
            new_rating = 100
        if new_rating <= 1:
            new_rating = 1
        ratingModel.stars = new_rating
        RatingModel.query.session.commit()
        return ratingModel.stars
