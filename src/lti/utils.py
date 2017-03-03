from uuid import uuid1

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse  # Python 2


def parse_qs(qs):
    return dict((k, v if len(v) > 1 else v[0])
        for k, v in urlparse.parse_qs(qs).items())


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
