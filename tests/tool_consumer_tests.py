from ims_lti_py import ToolConsumer
from test_helper import create_test_tc
import unittest

class TestToolConsumer(unittest.TestCase):
    def test_signature(self):
        '''
        Should generate correct oauth signature.
        '''
        tc = create_test_tc()
        result = tc.generate_launch_data()
        self.assertNotEqual(result, None)
        self.assertEqual(result['oauth_signature'],
                'o8Oh2XbGx5Wa1yvcEdsdOydoYV4=')

    def test_url_query_parameters(self):
        '''
        Should generate a correct signature with URL query parameters.
        '''
        tc = create_test_tc()
        tc.launch_url = 'http://dr-chuck.com/ims/php-simple/tool.php?a=1&b=2&c=3%20%26a'
        result = tc.generate_launch_data()
        self.assertNotEqual(result, None)
        self.assertEquals(result['oauth_signature'], 
                'kiObbrNVu4vHzd0+yVDHvrsvegQ=')
        self.assertEquals(result['c'], '3 &a')

    def test_signature_port(self):
        '''
        Should generate a correct signature with a non-standard port.
        '''
        tc = create_test_tc({'resource_link_id': 1})

        def test_url(url, sig):
            tc.launch_url = url
            ld = tc.generate_launch_data()
            self.assertNotEqual(ld, None)
            self.assertEquals(ld['oauth_signature'], sig)

        test_url('http://dr-chuck.com:123/ims/php-simple/tool.php',
                'I2zrOsXkLvBMbb5HzRXZrZAQVOg=')
        test_url('http://dr-chuck.com/ims/php-simple/tool.php',
                'L3VZIDWMLqBVqkGqpBLSjems/QY=')
        test_url('http://dr-chuck.com:80/ims/php-simple/tool.php',
                'L3VZIDWMLqBVqkGqpBLSjems/QY=')
        test_url('http://dr-chuck.com:443/ims/php-simple/tool.php',
                'NCkKyc8X+XbULcVTuHagTATxcLM=')
        test_url('https://dr-chuck.com/ims/php-simple/tool.php',
                'hjIv46SZHK8hEBF0n79Z8al47Oo=')
        test_url('https://dr-chuck.com:443/ims/php-simple/tool.php',
                'hjIv46SZHK8hEBF0n79Z8al47Oo=')
        test_url('https://dr-chuck.com:80/ims/php-simple/tool.php',
                '94N4Am1bvyInWNXM4WSNyoOMmUc=')
        test_url('https://dr-chuck.com:80/ims/php-simple/tool.php?oi=hoyt',
                'g724Rvpu1fC/kkb6sZEmzScUcLg=')

    def test_uri_query_parameters(self):
        '''
        Should include URI query parameters.
        '''
        tc = ToolConsumer('12345', 'secret', {
            'resource_link_id': 1,
            'user_id': 2
            })
        tc.launch_url = 'http://www.yahoo.com?a=1&b=2'
        result = tc.generate_launch_data()
        self.assertNotEqual(result, None)
        self.assertEqual(result['a'], '1')
        self.assertEqual(result['b'], '2')

    def test_overite_uri_query_parameters(self):
        '''
        Should not allow overwriting other parameters from the URI query
        string.
        '''
        tc = ToolConsumer('12345', 'secret', {
            'resource_link_id': 1,
            'user_id': 2
            })
        tc.launch_url = 'http://www.yahoo.com?user_id=123&lti_message_type=1234'
        result = tc.generate_launch_data()
        self.assertNotEqual(result, None)
        self.assertEqual(result['user_id'], '2')
        self.assertEqual(result['lti_message_type'],
                'basic-lti-launch-request')

    def test_allow_lti_version_in_params(self):
        '''
        Should not overwrite an LTI version passed in params
        '''
        tc = ToolConsumer('12345', 'secret', {
            'resource_link_id': 1,
            'user_id': 2,
            'lti_version': 'LTI-1.0p'
        })
        tc.launch_url = 'http://www.yahoo.com?user_id=123&lti_message_type=1234'
        result = tc.generate_launch_data()
        self.assertEqual(result['lti_version'], 'LTI-1.0')
