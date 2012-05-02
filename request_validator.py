class RequestValidator():
    def is_valid_request(self, request, handle_error = True):
        '''
        Validates an OAuth request using the python-oauth2 library:
            https://github.com/simplegeo/python-oauth2
        '''
        
