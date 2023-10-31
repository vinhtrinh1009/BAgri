class ThirdPartyRequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class NotSupported(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class ServiceError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class SchemaError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class OperationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ChainCodeOperationError(OperationError):
    def __init__(self, message, code, info=None):
        super().__init__(message)
        self.code = code
        self.info = info