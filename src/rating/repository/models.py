from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RatingModel(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    stars = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"<id='{self.id}', username='{self.username}', stars='{self.stars}'>"
