from domain.entities import Library
from dto.api.library_dto import LibraryAPI


def library_to_dto(library: Library) -> LibraryAPI:
    return LibraryAPI(
        library_uid=library.library_uid,
        name=library.name,
        city=library.city,
        address=library.address
    )
