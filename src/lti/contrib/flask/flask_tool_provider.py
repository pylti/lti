from lti import ToolProvider

class FlaskToolProvider(ToolProvider):
    '''
    ToolProvider that works with Flask requests
    '''
    @staticmethod
    def from_flask_request(secret=None, request=None):
        if request is None:
            raise ValueError('request must be supplied')

        params = request.form.copy()
        headers = request.headers.copy()
        url = request.url
        return ToolProvider.from_unpacked_request(secret, params, url, headers)
