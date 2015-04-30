import unittest

from dce_lti_py import LaunchParams, DEFAULT_LTI_VERSION, InvalidLTIConfigError
from dce_lti_py.launch_params import InvalidLaunchParamError

class TestLaunchParams(unittest.TestCase):

    def test_constructor(self):
        lp = LaunchParams()
        self.assertTrue(lp['lti_version'], DEFAULT_LTI_VERSION)
        self.assertTrue(lp['lti_message_type'], 'basic-lti-launch-request')

        lp = LaunchParams({
            'lti_version': 'LTI-foo',
            'lti_message_type': 'bar',
            'resource_link_id': 123
        })
        self.assertTrue(lp['resource_link_id'], 123)
        self.assertTrue(lp['lti_version'], 'LTI-foo')

        self.failUnlessRaises(InvalidLaunchParamError, LaunchParams, {
            'foo': 'bar'
        })


    def test_get_item(self):

        lp = LaunchParams()
        self.assertEqual(lp['lti_version'], DEFAULT_LTI_VERSION)
        with self.assertRaises(KeyError):
            foo = lp['foo']

    def test_set_item(self):
        lp = LaunchParams()
        lp['lti_version'] = 'bar'
        self.assertEqual(lp['lti_version'], 'bar')

    def test_list_params(self):

        lp = LaunchParams({'roles': 'foo,bar,baz'})
        self.assertEqual(lp['roles'], ['foo','bar','baz'])
        self.assertEqual(lp._params['roles'], 'foo,bar,baz')

        lp['roles'] = ['bar','baz']
        self.assertEqual(lp['roles'], ['bar','baz'])
        self.assertEqual(lp._params['roles'], 'bar,baz')

        lp['roles'] = 'blah, bluh '
        self.assertEqual(lp['roles'], ['blah','bluh'])

    def test_non_spec_params(self):
        lp = LaunchParams()
        lp.set_non_spec_param('foo', 'bar')
        self.assertEqual(lp.get_non_spec_param('foo'), 'bar')
        self.assertEqual(lp._params['foo'], 'bar')
        self.assertRaises(KeyError, lp.get('foo'))

    def test_dict_behavior(self):

        lp = LaunchParams({
            'lti_version': 'foo',
            'lti_message_type': 'bar'
        })
        self.assertEqual(len(lp), 2)
        lp.update({'resource_link_id': 1})
        self.assertEqual(len(lp), 3)

        self.failUnlessRaises(InvalidLaunchParamError, lp.update, {
            'foo': 'bar'
        })

        self.assertItemsEqual(
            lp.keys(),
            ['lti_version', 'lti_message_type', 'resource_link_id']
        )

        self.assertEqual(dict(lp), {
            'lti_version': 'foo',
            'lti_message_type': 'bar',
            'resource_link_id': 1
        })

