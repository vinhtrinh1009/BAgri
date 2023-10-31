from enum import IntEnum

class ChaincodeOpErrorStatus(IntEnum):
    PRE_ERROR = 0
    GENFILE_ERROR = 1
    PACKAGE_ERROR = 2
    GITLAB_ERROR = 3
    INSTALL_ERROR = 4
    DEPLOY_CHAINCODE = 5
    APPROVE_ERROR = 6
    COMMIT_ERROR = 7
    GEN_DOC_ERROR = 8
    UPLOAD_STORAGE_ERROR = 9
