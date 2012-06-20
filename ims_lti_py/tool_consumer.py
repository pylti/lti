from collections import defaultdict
from urlparse import urlparse

import textwrap
import oauth2

from launch_params import LaunchParamsMixin
from request_validator import RequestValidatorMixin
from utils import InvalidLTIConfigError

class ToolConsumer(LaunchParamsMixin, RequestValidatorMixin, object):
    def __init__(self, consumer_key, consumer_secret, params =
            defaultdict(lambda: None)):
        '''
        Create new ToolConsumer.
        '''
        super(ToolConsumer, self).__init__()

        # Prevent key errors
        params_dict = defaultdict(lambda: None)
        params_dict.update(params)

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.non_spec_params = defaultdict(lambda: None)

        self.launch_url = params_dict['launch_url']
        self.process_params(params_dict)

    def set_config(self, config):
        '''
        Set launch data from a ToolConfig.
        '''
        # TODO: Implement ToolConfig
        pass

    def has_required_params(self):
        '''
        Check if required parameters for a tool launch are set.
        '''
        return self.consumer_key and\
                self.consumer_secret and\
                self.launch_params['resource_link_id'] and\
                self.launch_url

    def generate_launch_data(self):
        # Validate params
        if not self.has_required_params():
            raise InvalidLTIConfigError(textwrap.dedent('ToolConsumer does not have all required attributes'))

        params = self.to_params()
        params['lti_version'] = 'LTI-1.0'
        params['lti_message_type'] = 'basic-lti-launch-request'

        # Parse URL to get host
        uri = urlparse(self.launch_url)

        if uri.port == None:
            host = uri.host
        else:
            host = uri.host + ':' + uri.port

        # Get new OAuth consumer
        consumer = oauth2.Consumer(key = self.options['consumer_key'],\
                secret = self.options['consumer_secret'])
        
        path = uri.path
        path = '/' if path == '' else path

        options = {
                'oauth_nonce': self.nonce,
                'oauth_timestamp': self.timestamp,
                'oauth_scheme': 'body'
                }
        request = oauth2.Request(method = 'POST', 
                url = self.launch_url,
                parameters = options)

        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method, consumer, None)

        # Request was made by an HTML form in the user's browser. Revert the
        # escapage and return the hash of post parameters ready for embedding
        # in an html view.
        dic = {}
        for param in request.body.split('&'):
            for key, val in param.split('='):
                dic[key] = val
        return dic
