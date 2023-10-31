import enum

class NetworkError(enum.Enum):
    CLUSTER_CREATE_ERROR = 1
    CLUSTER_CREATE_TIMEOUT = 2
    OPERATION_ERROR = 3
