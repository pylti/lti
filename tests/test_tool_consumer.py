from lti import ToolConsumer, LaunchParams
from lti.utils import parse_qs, InvalidLTIConfigError
import unittest

from oauthlib.common import generate_client_id, generate_token, unquote
from requests import PreparedRequest

class TestToolConsumer(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        client_id = generate_client_id()
        client_secret = generate_token()
        tc = ToolConsumer(client_id, client_secret,
                          launch_url='http://example.edu')
        self.assertIsInstance(tc.launch_params, LaunchParams)

        lp = LaunchParams()
        tc = ToolConsumer(client_id, client_secret,
                          launch_url='http://example.edu', params=lp)
        self.assertEqual(tc.launch_params, lp)

        lp_dict = {'resource_link_id': 1}
        tc = ToolConsumer(client_id, client_secret,
                          launch_url='http://example.edu',
                          params=lp_dict)
        self.assertIsInstance(tc.launch_params, LaunchParams)
        self.assertEqual(tc.launch_params._params.get('resource_link_id'), 1)

        # no launch_url should raise exception
        self.failUnlessRaises(InvalidLTIConfigError, ToolConsumer,
                              client_id, client_secret,
                              params=lp_dict)

        # but confirm that 'launch_url' can still be passed in params
        # (backwards compatibility)
        lp_dict['launch_url'] = 'http://example.edu'
        tc = ToolConsumer(client_id, client_secret, params=lp_dict)
        self.assertEqual(tc.launch_url, 'http://example.edu')

    def test_has_required_params(self):

        client_id = generate_client_id()
        client_secret = generate_token()
        tc = ToolConsumer(client_id, client_secret,
                          launch_url='http://example.edu')

        self.assertFalse(tc.has_required_params())

        tc.launch_params['resource_link_id'] = generate_token()
        self.assertTrue(tc.has_required_params())

    def test_generate_launch_request(self):
        launch_params = {
            'lti_version': 'foo',
            'lti_message_type': 'bar',
            'resource_link_id': 'baz'
        }
        tc = ToolConsumer('client_key', 'client_secret',
                          launch_url='http://example.edu/',
                          params=launch_params)
        launch_req = tc.generate_launch_request(nonce='abcd1234',
                                                timestamp='1234567890')

        self.assertIsInstance(launch_req, PreparedRequest)

        got = parse_qs(unquote(launch_req.body.decode('utf-8')))
        correct = launch_params.copy()
        correct.update({
            'oauth_nonce': 'abcd1234',
            'oauth_timestamp': '1234567890',
            'oauth_version': '1.0',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_consumer_key': 'client_key',
            'oauth_signature': 'u2xlj 1gF4y 6gKHNeiL9cN3tOI=',
        })

        self.assertEqual(got, correct)

    def test_launch_request_with_qs(self):
        """
        test that qs params in launch url are ok
        """
        launch_params = {
            'lti_version': 'abc',
            'lti_message_type': 'def',
            'resource_link_id': '123'
        }
        tc = ToolConsumer('client_key', 'client_secret',
                          launch_url='http://example.edu/foo?bar=1',
                          params=launch_params)
        launch_req = tc.generate_launch_request(nonce='wxyz7890',
                                                timestamp='2345678901')
        got = parse_qs(unquote(launch_req.body.decode('utf-8')))
        correct = launch_params.copy()
        correct.update({
            'oauth_nonce': 'wxyz7890',
            'oauth_timestamp': '2345678901',
            'oauth_version': '1.0',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_consumer_key': 'client_key',
            'oauth_signature': 'UH2l86Wq/g5Mu64GpCRcec6tEYY=',
            })
        self.assertEqual(got, correct)

    def test_generate_launch_data(self):
        launch_params = {
            'lti_version': 'abc',
            'lti_message_type': 'def',
            'resource_link_id': '123'
        }
        tc = ToolConsumer('client_key', 'client_secret',
                          launch_url='http://example.edu/',
                          params=launch_params)
        got = tc.generate_launch_data(nonce='wxyz7890',
                                      timestamp='2345678901')
        correct = launch_params.copy()
        correct.update({
            'oauth_nonce': 'wxyz7890',
            'oauth_timestamp': '2345678901',
            'oauth_version': '1.0',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_consumer_key': 'client_key',
            'oauth_signature': 'gXIAk60dLsrh6YQGT5ZGK6tHDGY=',
            })
        self.assertEqual(got, correct)
