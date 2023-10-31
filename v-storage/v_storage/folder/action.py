import enum

class FolderAction(enum.Enum):
    CREATE = 1
    UPLOAD = 2
    RENAME = 3
    MOVE = 4
    COPY = 5
    FAVORITE = 6
    UNFAVORITE = 7
    TRASH = 8
    UNTRASH = 9
    DELETE = 10