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
        self.oauth_consumer = oauth2.Consumer(
            self.consumer_key, self.consumer_secret)

    def is_valid_request(self, request, parameters={},
                         fake_method=None, handle_error=True):
        '''
        Validates an OAuth request using the python-oauth2 library:
            https://github.com/simplegeo/python-oauth2

        '''
        try:
            # Set the parameters to be what we were passed earlier
            # if we didn't get any passed to us now
            if not parameters and hasattr(self, 'params'):
                parameters = self.params

            method, url, headers, parameters = self.parse_request(
                request, parameters, fake_method)

            oauth_request = oauth2.Request.from_request(
                method,
                url,
                headers=headers,
                parameters=parameters)

            self.oauth_server.verify_request(
                oauth_request, self.oauth_consumer, {})

        except oauth2.MissingSignature, e:
            if handle_error:
                return False
            else:
                raise e
        # Signature was valid
        return True

    def parse_request(self, request, parameters):
        '''
        This must be implemented for the framework you're using

        Returns a tuple: (method, url, headers, parameters)
        method is the HTTP method: (GET, POST)
        url is the full absolute URL of the request
        headers is a dictionary of any headers sent in the request
        parameters are the parameters sent from the LMS
        '''
        raise NotImplemented

    def valid_request(self, request):
        '''
        Check whether the OAuth-signed request is valid and throw error if not.
        '''
        self.is_valid_request(request, parameters={}, handle_error=False)


class FlaskRequestValidatorMixin(RequestValidatorMixin):
    '''
    A mixin for OAuth request validation using Flask
    '''

    def parse_request(self, request, parameters=None, fake_method=None):
        '''
        Parse Flask request
        '''
        return (request.method,
                request.url,
                request.headers,
                request.form.copy())


class DjangoRequestValidatorMixin(RequestValidatorMixin):
    '''
    A mixin for OAuth request validation using Django
    '''

    def parse_request(self, request, parameters, fake_method=None):
        '''
        Parse Django request
        '''
        return (fake_method or request.method,
                request.build_absolute_uri(),
                request.META,
                (dict(request.POST.iteritems())
                    if request.method == 'POST'
                    else parameters))
