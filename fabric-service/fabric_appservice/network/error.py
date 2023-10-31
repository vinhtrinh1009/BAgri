import enum

class NetworkCreateErrorStatus(enum.Enum):
    UNFIXABLE_ERROR = 1
    CLUSTER_CREATE_ERROR = 2
    CLUSTER_CREATE_TIMEOUT = 3
    OPERATION_ERROR = 4

class NetworkUpdateErrorStatus(enum.Enum):
    UNFIXABLE_ERROR = 1
    CLUSTER_ERROR = 2
    SUBMIT_UPDATE = 3
    INSTALL_DAPP = 4
