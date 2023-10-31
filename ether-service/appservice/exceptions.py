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