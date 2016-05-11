from lti import ToolProvider

class FlaskToolProvider(ToolProvider):
    '''
    ToolProvider that works with Flask requests
    '''
    @staticmethod
    def from_flask_request(secret, request):
        params = request.form.copy()
        headers = request.headers.copy()
        url = request.url
        return ToolProvider.from_unpacked_request(secret, params, url, headers)
