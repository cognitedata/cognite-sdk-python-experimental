from enum import Enum


class StrEnum(str, Enum):
    """
    Use enum with strings in the following way:
    NORTH = 'north',    # notice the trailing comma
    SOUTH = 'south'
    """

    def __str__(self) -> str:
        return self.value  # type: ignore[no-any-return]
