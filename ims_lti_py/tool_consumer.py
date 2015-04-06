
from requests import Request
from oauthlib.common import unquote
from requests_oauthlib import OAuth1
from requests_oauthlib.oauth1_auth import SIGNATURE_TYPE_BODY

from tool_base import ToolBase
from launch_params import LAUNCH_PARAMS_REQUIRED
from utils import parse_qs, InvalidLTIConfigError, generate_identifier

class ToolConsumer(ToolBase):

    def __init__(self, consumer_key, consumer_secret,
                 params=None, launch_url=None):
        '''
        Create new ToolConsumer.
        '''
        # allow launch_url to be specified in launch_params for
        # backwards compatibility
        if launch_url is None:
            if 'launch_url' not in params:
                raise InvalidLTIConfigError('missing \'launch_url\' arg!')
            else:
                launch_url = params['launch_url']
                del params['launch_url']
        self.launch_url = launch_url

        super(ToolConsumer, self).__init__(consumer_key, consumer_secret,
                                           params=params)

    def has_required_params(self):
        return all([
            self.launch_params.get(x) for x in LAUNCH_PARAMS_REQUIRED
        ])

    def generate_launch_request(self, **kwargs):
        """
        returns a Oauth v1 "signed" requests.PreparedRequest instance
        """

        if not self.has_required_params():
            raise InvalidLTIConfigError(
                'Consumer\'s launch params missing one of ' \
                + str(LAUNCH_PARAMS_REQUIRED)
            )

#        if 'oauth_consumer_key' not in self.launch_params:
#            self.launch_params['oauth_consumer_key'] = self.consumer_key

        params = self.to_params()
        r = Request('POST', self.launch_url, data=params).prepare()
        sign = OAuth1(self.consumer_key, self.consumer_secret,
                                signature_type=SIGNATURE_TYPE_BODY, **kwargs)
        return sign(r)

    def generate_launch_data(self, **kwargs):
        """
        Provided for backwards compatibility
        """

        r = self.generate_launch_request(**kwargs)
        return parse_qs(unquote(r.body))

    def set_config(self, config):
        '''
        Set launch data from a ToolConfig.
        '''
        if self.launch_url == None:
            self.launch_url = config.launch_url
            self.launch_params.update(config.custom_params)

