from test_helper import create_test_tc
import unittest

class TestToolConsumer(unittest.TestCase):
    def testSignature(self):
        tc = create_test_tc()
        result = tc.generate_launch_data()
        self.assertEqual(result['oauth_signature'],
                'TPFPK4u3NwmtLt0nDMP1G1zG30U=')
