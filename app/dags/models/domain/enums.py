from enum import Enum, auto


class STATUS(Enum):
    IN_PROGRESS = auto()
    FINISHED = auto()
    FAILED = auto()
