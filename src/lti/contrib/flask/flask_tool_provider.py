from lti import ToolProvider


class FlaskToolProvider(ToolProvider):
    '''
    ToolProvider that works with Flask requests
    '''
    @classmethod
    def from_flask_request(cls, secret=None, request=None):
        if request is None:
            raise ValueError('request must be supplied')

        params = request.form.copy()
        headers = dict(request.headers)
        url = request.url
        return cls.from_unpacked_request(secret, params, url, headers)
