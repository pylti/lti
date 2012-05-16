from test_helper import create_test_tc
import unittest

class TestToolConsumer(unittest.TestCase):
    def testSignature(self):
        tc = create_test_tc()
        result = tc.generate_launch_data()
        self.assertEqual(result['oauth_signature'],
                'TPFPK4u3NwmtLt0nDMP1G1zG30U=')

    def testURLQueryParameters(self):
        tc = create_test_tc()
        tc.launch_url = 'http://dr-chuck.com/ims/php-simple/tool.php?a=1&b=2&c=3%20%26a'
        result = tc.generate_launch_data()
        self.assetEquals(result['oauth_signature'], 
                'uF7LooyefQN5aocx7UlYQ4tQM5k=')
        self.assertEquals(result['c'], '3 &a')

