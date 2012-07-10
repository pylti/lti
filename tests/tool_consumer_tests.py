from ims_lti_py import ToolConsumer
from test_helper import create_test_tc
import unittest

class TestToolConsumer(unittest.TestCase):
    # TODO: These cases keep failing since we generate a random nonce and use
    # the current timestamp inside of ToolConsumer. Replace this with generated
    # members, and generate them here to actually implement these tests.
    def test_signature(self):
        '''
        Should generate correct oauth signature.
        '''
        tc = create_test_tc()
        result = tc.generate_launch_data()
        self.assertNotEqual(result, None)
        self.assertEqual(result['oauth_signature'],
                'ZXogq5KUR0ukZijtSjt4qh/S4Vc=')

    def test_url_query_parameters(self):
        '''
        Should generate a correct signature with URL query parameters.
        '''
        tc = create_test_tc()
        tc.launch_url = 'http://dr-chuck.com/ims/php-simple/tool.php?a=1&b=2&c=3%20%26a'
        result = tc.generate_launch_data()
        self.assertNotEqual(result, None)
        self.assertEquals(result['oauth_signature'], 
                'lpi9xKVVXZB6xewfh/PUeasHiwU=')
        self.assertEquals(result['c'], '3 &a')

    def test_signature_port(self):
        '''
        Should generate a correct signature with a non-standard port.
        '''
        tc = ToolConsumer('12345', 'secret', {'resource_link_id': 1})
        tc.timestamp = '1251600739'
        tc.nonce = 'c8350c0e47782d16d2fa48b2090c1d8f'

        def test_url(url, sig):
            tc.launch_url = url
            ld = tc.generate_launch_data()
            self.assertNotEqual(ld, None)
            self.assertEquals(ld['oauth_signature'], sig)

        test_url('http://dr-chuck.com:123/ims/php-simple/tool.php',
                'Y/QdFIdVeGkXnnT77h8FXaSp4T4=')
        test_url('http://dr-chuck.com/ims/php-simple/tool.php',
                'mSoeJJMmtFCmMYgpHZ8hCnc5Gzo=')
        test_url('http://dr-chuck.com:80/ims/php-simple/tool.php',
                'mSoeJJMmtFCmMYgpHZ8hCnc5Gzo=')
        test_url('http://dr-chuck.com:443/ims/php-simple/tool.php',
                'KaISX3G2Q+zHW/BZI1vNKyGoblo=')
        test_url('https://dr-chuck.com/ims/php-simple/tool.php',
                'yCtVB+/6njhnKKzxvYkIR8hUD3Q=')
        test_url('https://dr-chuck.com:443/ims/php-simple/tool.php',
                'yCtVB+/6njhnKKzxvYkIR8hUD3Q=')
        test_url('https://dr-chuck.com:80/ims/php-simple/tool.php',
                'tz94qHbVCmx2u/PZyO4l0XXWU+s=')
        test_url('https://dr-chuck.com:80/ims/php-simple/tool.php?oi=hoyt',
                'jRCj3U8JwHI4rEsgNMihOSE8xCQ=')

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
