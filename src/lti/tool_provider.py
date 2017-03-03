from .utils import InvalidLTIRequestError
from .launch_params import LaunchParams
from .tool_base import ToolBase

from oauthlib.oauth1 import SignatureOnlyEndpoint
from oauthlib.oauth1.rfc5849 import CONTENT_TYPE_FORM_URLENCODED
from requests.structures import CaseInsensitiveDict

from .outcome_request import OutcomeRequest
from collections import defaultdict

try:
    from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
except ImportError:
    # Python 2
    from urllib import urlencode
    from urlparse import urlsplit, urlunsplit, parse_qsl


class ToolProvider(ToolBase):
    '''
    Implements the LTI Tool Provider.
    '''

    @classmethod
    def from_unpacked_request(cls, secret, params, url, headers):

        launch_params = LaunchParams(params)

        if 'oauth_consumer_key' not in launch_params:
            raise InvalidLTIRequestError("oauth_consumer_key not found!")

        return cls(consumer_key=launch_params['oauth_consumer_key'],
                   consumer_secret=secret, params=launch_params,
                   launch_url=url, launch_headers=headers)

    def __init__(self, consumer_key=None, consumer_secret=None, params=None,
                 launch_url=None, launch_headers=None):

        super(ToolProvider, self).__init__(consumer_key, consumer_secret,
                                           params=params)
        self.outcome_requests = []
        self._last_outcome_request = None
        self.launch_url = launch_url
        self.launch_headers = launch_headers or CaseInsensitiveDict()
        if 'Content-Type' not in self.launch_headers:
            self.launch_headers['Content-Type'] = CONTENT_TYPE_FORM_URLENCODED

    def is_valid_request(self, validator):
        validator = ProxyValidator(validator)
        endpoint = SignatureOnlyEndpoint(validator)

        valid, request = endpoint.validate_request(
            self.launch_url,
            'POST',
            self.to_params(),
            self.launch_headers
        )

        if valid and not self.consumer_key and not self.consumer_secret:
            # Gather the key and secret
            self.consumer_key = self.launch_params['oauth_consumer_key']
            self.consumer_secret = validator.secret

        return valid

    def is_outcome_service(self):
        '''
        Check if the Tool Launch expects an Outcome Result.
        '''
        return self.launch_params.get('lis_outcome_service_url') and \
            self.launch_params.get('lis_result_sourcedid')

    def username(self, default=None):
        '''
        Return the full, given, or family name if set.
        '''
        for item in ['lis_person_name_given',
                     'lis_person_name_family',
                     'lis_person_name_full']:
            if item in self.launch_params:
                return self.launch_params[item]
        return default

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

    def post_replace_result(self, score, outcome_opts=defaultdict(lambda: None), result_data=None):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult.

        Returns OutcomeResponse object and stores it in self.outcome_request

        OPTIONAL:
            result_data must be a dictionary
            Note: ONLY ONE of these values can be in the dict at a time,
            due to the Canvas specification.

            'text' : str text
            'url' : str url
        '''
        return self.new_request(outcome_opts).post_replace_result(score, result_data)

    def post_delete_result(self, outcome_opts=defaultdict(lambda: None)):
        '''
        POSTs a delete request to the Tool Consumer.
        '''
        return self.new_request(outcome_opts).post_delete_result()

    def post_read_result(self, outcome_opts=defaultdict(lambda: None)):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult, the
        returned OutcomeResponse will have the score.
        '''
        return self.new_request(outcome_opts).post_read_result()

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
        return all((self._last_outcome_request,
                    self._last_outcome_request.was_outcome_post_successful()))

    def new_request(self, defaults):
        opts = dict(defaults)
        opts.update({
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'lis_outcome_service_url': self.lis_outcome_service_url,
            'lis_result_sourcedid': self.lis_result_sourcedid
        })
        self.outcome_requests.append(OutcomeRequest(opts=opts))
        self._last_outcome_request = self.outcome_requests[-1]
        return self._last_outcome_request


class ProxyValidator(object):
    '''
    Proxies a RequestValidator to save the client secret.
    '''

    def __init__(self, validator):
        self._validator = validator

    def __getattr__(self, name):
        value = getattr(self._validator, name)
        if name == 'get_client_secret':
            def save_secret(*args, **kwargs):
                self.secret = value(*args, **kwargs)
                return self.secret
            return save_secret
        return value
