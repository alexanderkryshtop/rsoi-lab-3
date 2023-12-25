from dataclasses import dataclass
from uuid import UUID


@dataclass
class LibraryAPI:
    library_uid: UUID
    name: str
    city: str
    address: str

    def to_dict(self) -> dict:
        return {
            "libraryUid": self.library_uid,
            "name": self.name,
            "city": self.city,
            "address": self.address,
        }
