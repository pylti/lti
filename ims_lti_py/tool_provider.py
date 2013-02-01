from launch_params import LaunchParamsMixin
from request_validator import RequestValidatorMixin, \
    FlaskRequestValidatorMixin, DjangoRequestValidatorMixin
from outcome_request import OutcomeRequest
from collections import defaultdict
import re
from urllib import urlencode
from urlparse import urlsplit, urlunsplit

try:
    from urlparse import parse_qsl
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qsl  # NOQA


accessors = [
    'consumer_key',
    'consumer_secret',
    'outcome_requests',
    'lti_errormsg',
    'lti_errorlog',
    'lti_msg',
    'lti_log'
]


class ToolProvider(LaunchParamsMixin, RequestValidatorMixin, object):
    '''
    Implements the LTI Tool Provider.
    '''

    def __init__(self, consumer_key, consumer_secret, params={}):
        '''
        Create new ToolProvider.
        '''
        # Initialize all class accessors to None
        for param in accessors:
            setattr(self, param, None)

        # These are hyper important class members that we init first
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        # Call superclass initializers
        super(ToolProvider, self).__init__()

        self.non_spec_params = defaultdict(lambda: None)
        self.outcome_requests = []
        self.params = params
        self.process_params(params)

    def has_role(self, role):
        '''
        Check whether the Launch Paramters set the role.
        '''
        return self.roles and any([re.search(role, our_role, re.I)
                                   for our_role in self.roles])

    def is_student(self):
        '''
        Convenience method for checking if the user has 'learner' or 'student'
        role.
        '''
        return any((self.has_role('learner'),
                    self.has_role('student')))

    def is_instructor(self):
        '''
        Convenience method for checking if user has 'instructor', 'faculty'
        or 'staff' role.

        Currently this does not support the TeachingAssistant role
        '''
        return any((self.has_role('instructor'),
                    self.has_role('faculty'),
                    self.has_role('staff')))

    def is_launch_request(self):
        '''
        Check if the request was an LTI Launch Request.
        '''
        return self.lti_message_type == 'basic-lti-launch-request'

    def is_outcome_service(self):
        '''
        Check if the Tool Launch expects an Outcome Result.
        '''
        return (self.lis_outcome_service_url and
                self.lis_result_sourcedid)

    def username(self, default=None):
        '''
        Return the full, given, or family name if set.
        '''
        if self.lis_person_name_given:
            return self.lis_person_name_given
        elif self.lis_person_name_family:
            return self.lis_person_name_family
        elif self.lis_person_name_full:
            return self.lis_person_name_full
        else:
            return default

    def post_replace_result(self, score):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult.

        Returns OutcomeResponse object and stores it in self.outcome_request
        '''
        return self.new_request().post_replace_result(score)

    def post_delete_result(self):
        '''
        POSTs a delete request to the Tool Consumer.
        '''
        return self.new_request().post_delete_result()

    def post_read_result(self):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult, the
        returned OutcomeResponse will have the score.
        '''
        return self.new_request().post_read_result()

    def last_outcome_request(self):
        '''
        Returns the most recent OutcomeRequest.
        '''
        return self.outcome_requests[-1]

    def last_outcome_success(self):
        '''
        Convenience method for determining the success of the last
        OutcomeRequest.
        '''
        return all((self.last_outcome_request,
                    self.last_outcome_request.was_outcome_post_successful()))

    def build_return_url(self):
        '''
        If the Tool Consumer sent a return URL, add any set messages to the
        URL.
        '''
        if not self.launch_presentation_return_url:
            return None

        lti_message_fields = ['lti_errormsg', 'lti_errorlog',
                              'lti_msg', 'lti_log']

        messages = dict([(key, getattr(self, key))
                         for key in lti_message_fields
                         if getattr(self, key, None)])

        # Disassemble original return URL and reassemble with our options added
        original = urlsplit(self.launch_presentation_return_url)

        combined = messages.copy()
        combined.update(dict(parse_qsl(original.query)))

        combined_query = urlencode(combined)

        return urlunsplit((
            original.scheme,
            original.netloc,
            original.path,
            combined_query,
            original.fragment
        ))

    def new_request(self):
        opts = defaultdict(lambda: None)
        opts = {
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'lis_outcome_service_url': self.lis_outcome_service_url,
            'lis_result_sourcedid': self.lis_result_sourcedid
        }
        self.outcome_requests.append(OutcomeRequest(opts=opts))
        self.last_outcome_request = self.outcome_requests[-1]
        return self.last_outcome_request


class DjangoToolProvider(DjangoRequestValidatorMixin, ToolProvider):
    '''
    OAuth ToolProvider that works with Django requests
    '''

    def success_redirect(self, msg='', log=''):
        '''
        Shortcut for redirecting Django view to LTI Consumer with messages
        '''
        from django.shortcuts import redirect
        self.lti_msg = msg
        self.lti_log = log
        return redirect(self.build_return_url())

    def error_redirect(self, errormsg='', errorlog=''):
        '''
        Shortcut for redirecting Django view to LTI Consumer with errors
        '''
        from django.shortcuts import redirect
        self.lti_errormsg = errormsg
        self.lti_errorlog = errorlog
        return redirect(self.build_return_url())


class FlaskToolProvider(FlaskRequestValidatorMixin, ToolProvider):
    '''
    OAuth ToolProvider that works with Flask requests
    '''
    pass
