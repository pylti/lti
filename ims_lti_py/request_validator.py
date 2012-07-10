import oauth2

class RequestValidatorMixin(object):
    '''
    A 'mixin' for OAuth request validation.
    '''
    def __init__(self):
        super(RequestValidatorMixin, self).__init__()

        self.oauth_server = oauth2.Server()
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        self.oauth_server.add_signature_method(signature_method)
        self.oauth_consumer = oauth2.Consumer(self.consumer_key,
                self.consumer_secret)

    def is_valid_request(self, request, handle_error = True):
        '''
        Validates an OAuth request using the python-oauth2 library:
            https://github.com/simplegeo/python-oauth2

        '''
        try:
            params = {}
            if len(request.form) > 1:
                for key in request.form:
                    params[key] = request.form[key]

            oauth_request = oauth2.Request.from_request(
                    request.method, 
                    request.url,
                    headers = request.headers,
                    parameters = params)
            self.oauth_server.verify_request(oauth_request, 
                    self.oauth_consumer, {})
        except oauth2.MissingSignature, e:
            if handle_error:
                return False
            else:
                raise e
        # Signature was valid
        return True

    def valid_request(self, request):
        '''
        Check whether the OAuth-signed request is valid and throw error if not.
        '''
        self.is_valid_request(request, False)
