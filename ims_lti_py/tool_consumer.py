from collections import defaultdict
from urllib2 import urlparse, unquote

import oauth2
import time

from launch_params import LaunchParamsMixin
from request_validator import RequestValidatorMixin
from utils import InvalidLTIConfigError, generate_identifier

accessors = [
    'consumer_key',
    'consumer_secret',
    'launch_url',
]

class ToolConsumer(LaunchParamsMixin, RequestValidatorMixin, object):
    def __init__(self, consumer_key, consumer_secret, params = {}):
        '''
        Create new ToolConsumer.
        '''
        # Initialize all class accessors to None
        for opt in accessors:
            setattr(self, opt, None)

        # These are hyper important class members that we init first
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        # Call superclass initializers
        super(ToolConsumer, self).__init__()

        self.non_spec_params = defaultdict(lambda: None)

        self.launch_url = params.get('launch_url')
        self.process_params(params)

    def set_config(self, config):
        '''
        Set launch data from a ToolConfig.
        '''
        if self.launch_url == None:
            self.launch_url = config.launch_url
            self.custom_params.update(config.custom_params)

    def has_required_params(self):
        '''
        Check if required parameters for a tool launch are set.
        '''
        return self.consumer_key and\
                self.consumer_secret and\
                self.resource_link_id and\
                self.launch_url

    def generate_launch_data(self):
        # Validate params
        if not self.has_required_params():
            raise InvalidLTIConfigError('ToolConsumer does not have all required attributes: consumer_key = %s, consumer_secret = %s, resource_link_id = %s, launch_url = %s' %(self.consumer_key, self.consumer_secret, self.resource_link_id, self.launch_url))

        params = self.to_params()

        if not params.get('lit_version', None):
            params['lti_version'] = 'LTI-1.0'

        params['lti_message_type'] = 'basic-lti-launch-request'

        # Get new OAuth consumer
        consumer = oauth2.Consumer(key = self.consumer_key,\
                secret = self.consumer_secret)

        params.update({
            'oauth_nonce': str(generate_identifier()),
            'oauth_timestamp': str(int(time.time())),
            'oauth_scheme': 'body',
            'oauth_consumer_key': consumer.key
        })

        uri = urlparse.urlparse(self.launch_url)
        if uri.query != '':
            for param in uri.query.split('&'):
                key, val = param.split('=')
                if params.get(key) == None:
                    params[key] = str(val)

        request = oauth2.Request(method = 'POST', 
                url = self.launch_url,
                parameters = params)

        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method, consumer, None)

        # Request was made by an HTML form in the user's browser.
        # Return the dict of post parameters ready for embedding
        # in an html view.
        return_params = {}
        for key in request:
            if request[key] == None:
                return_params[key] = None
            elif isinstance(request[key], list):
                return_params[key] = request.get_parameter(key)
            else:
                return_params[key] = unquote(request.get_parameter(key))
        return return_params
