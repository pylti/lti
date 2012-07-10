from uuid import uuid1

def generate_identifier():
    return uuid1().__str__()

class InvalidLTIConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidLTIRequestError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
