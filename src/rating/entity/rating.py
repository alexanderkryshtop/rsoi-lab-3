from dataclasses import dataclass


@dataclass
class Rating:
    id: int
    username: str
    stars: int
