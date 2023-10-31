class ThirdPartyRequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class NetworkError(ThirdPartyRequestError):
    def __init__(self, message):
        super().__init__(message)

class StorageServiceRequestError(ThirdPartyRequestError):
    def __init__(self, message):
        super().__init__(message)

class EncryptionError(ThirdPartyRequestError):
    def __init__(self, message):
        super().__init__(message)

class SchemaError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class SdkError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)