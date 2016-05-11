
import unittest
from oauthlib.common import generate_client_id, generate_token
from lti import LaunchParams, ToolBase, DEFAULT_LTI_VERSION


def create_tb(key=None, secret=None, lp=None):
    key = key or generate_client_id()
    secret = secret or generate_token()
    lp = lp or LaunchParams()
    return ToolBase(key, secret, lp)

class TestToolBase(unittest.TestCase):

    def test_constructor(self):
        tb = create_tb()
        self.assertIsInstance(tb.launch_params, LaunchParams)

        lp = LaunchParams({'resource_link_id': 1})
        tb = create_tb(lp=lp)
        self.assertEqual(tb.launch_params, lp)

        lp_dict = {'resource_link_id': 3}
        tb = create_tb(lp=lp_dict)
        self.assertEqual(tb.launch_params['resource_link_id'], 3)

    def test_get_attr(self):

        tb = create_tb()
        self.assertEqual(tb.lti_version, DEFAULT_LTI_VERSION)
        resource_link_id = generate_token()
        tb = create_tb(lp={'resource_link_id': resource_link_id})
        self.assertEqual(tb.resource_link_id, resource_link_id)

        # should raise AttributeError for attributes that are not valid params
        with self.assertRaises(AttributeError) as cm:
            foo = tb.foo

        # otherwise return None
        self.assertIsNone(tb.context_id)

    def test_set_attr(self):
        tb = create_tb()
        tb.foo = 'bar'
        self.assertTrue('foo' in tb.__dict__)
        tb.context_id = 2345
        self.assertFalse('context_id' in tb.__dict__)
        self.assertEqual(tb.launch_params['context_id'], 2345)

    def test_has_role(self):

        tb = create_tb(lp={'roles': 'foo,bar,BLERG'})
        self.assertTrue(tb.has_role('foo'))
        self.assertTrue(tb.has_role('FOO'))
        self.assertTrue(tb.has_role('blerg'))
        self.assertFalse(tb.has_role('baz'))

    def test_is_student(self):

        tb = create_tb(lp={'roles': 'foo, student'})
        self.assertTrue(tb.is_student())

        tb = create_tb(lp={'roles': 'bar,Learner'})
        self.assertTrue(tb.is_student())

        tb = create_tb(lp={'roles': 'foo,bar'})
        self.assertFalse(tb.is_student())

    def test_is_instructor(self):

        tb = create_tb(lp={'roles': 'foo,staff'})
        self.assertTrue(tb.is_instructor())

        tb = create_tb(lp={'roles': 'foo, student'})
        self.assertFalse(tb.is_instructor())

    def test_is_launch_request(self):

        tb = create_tb()
        self.assertTrue(tb.is_launch_request())

        tb = create_tb(lp={'lti_message_type': 'foo'})
        self.assertFalse(tb.is_launch_request())

    def test_custom_ext_params(self):

        tb = create_tb()
        tb.set_custom_param('foo', 'bar')
        self.assertEqual(tb.launch_params['custom_foo'], 'bar')
        self.assertEqual(tb.get_custom_param('foo'), 'bar')

        tb.set_ext_param('baz', 'blergh')
        self.assertEqual(tb.launch_params['ext_baz'], 'blergh')
        self.assertEqual(tb.get_ext_param('baz'), 'blergh')
