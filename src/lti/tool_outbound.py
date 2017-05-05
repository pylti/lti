
from requests import Request
from requests_oauthlib import OAuth1
from requests_oauthlib.oauth1_auth import SIGNATURE_TYPE_BODY

from .tool_base import ToolBase
from .launch_params import LAUNCH_PARAMS_REQUIRED
from .utils import parse_qs, InvalidLTIConfigError


class ToolOutbound(ToolBase):

    def __init__(self, consumer_key, consumer_secret,
                 params=None, launch_url=None):
        '''
        Create new Outbound Tool.
        See ToolConsumer and ContentItemResponse for examples
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

        super(ToolOutbound, self).__init__(consumer_key, consumer_secret,
                                           params=params)

    def has_required_params(self):
        return True

    def generate_launch_request(self, **kwargs):
        """
        returns a Oauth v1 "signed" requests.PreparedRequest instance
        """

        if not self.has_required_params():
            raise InvalidLTIConfigError(
                'Consumer\'s launch params missing one of '
                + str(LAUNCH_PARAMS_REQUIRED)
            )

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
        return parse_qs(r.body.decode('utf-8'))