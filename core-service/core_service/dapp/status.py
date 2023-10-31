import enum


class DappStatus(enum.Enum):
    CREATE_PENDING = 1
    CREATE_FAIL = 2
    CREATED = 3
    DELETE_PENDING = 4
    DELETE_FAIL = 5
    UPDATE_PENDING = 6
    UPDATE_FAIL = 7
