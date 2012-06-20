import oauth2

class RequestValidatorMixin():
    '''
    A 'mixin' for OAuth request validation.
    '''
    def __init__(self):
        self.oauth_server = oauth2.Server()
        self.oath_consumer = oauth2.Consumer(self.consumer_key,
                self.consumer_secret)

    def is_valid_request(self, request, handle_error = True):
        '''
        Validates an OAuth request using the python-oauth2 library:
            https://github.com/simplegeo/python-oauth2

        '''
        try:
            self.oauth_server.verify_request(request, self.consumer)
        except oauth2.MissingSignature, e:
            if handle_error:
                return False
            else:
                raise e

    def valid_request(self, request):
        '''
        Check whether the OAuth-signed request is valid and throw error if not.
        '''
        self.is_valid_request(request, False)

    def request_oauth_nonce(self):
        '''
        Convenience method for getting the oauth nonce from the request.
        '''
        return self.oauth_signature_validator\
                and self.oath_signature_validator.request.oath_nonce

    def request_oauth_timestamp(self):
        '''
        Convenience method for getting the oath timestamp from the request.
        '''
        return self.oath_signature_validator\
                and self.oauth_signature_validator.request.oauth_timestamp
