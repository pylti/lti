
from lti import ToolProvider
from django.shortcuts import redirect

class DjangoToolProvider(ToolProvider):
    '''
    ToolProvider that works with Django requests
    '''
    @staticmethod
    def from_django_request(secret, request):
        params = request.POST.copy()
        # django shoves a bunch of other junk in META that we don't care about
        headers = dict([(k, request.META[k])
                        for k in request.META if \
                        k.upper().startswith('HTTP_') or \
                        k.upper().startswith('CONTENT_')])
        url = request.build_absolute_uri()
        return ToolProvider.from_unpacked_request(secret, params, url, headers)

    def success_redirect(self, msg='', log=''):
        '''
        Shortcut for redirecting Django view to LTI Consumer with messages
        '''
        self.lti_msg = msg
        self.lti_log = log
        return redirect(self.build_return_url())

    def error_redirect(self, errormsg='', errorlog=''):
        '''
        Shortcut for redirecting Django view to LTI Consumer with errors
        '''
        self.lti_errormsg = errormsg
        self.lti_errorlog = errorlog
        return redirect(self.build_return_url())
