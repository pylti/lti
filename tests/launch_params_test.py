from test_helper import create_test_tp, create_test_tc, create_params_tp

import unittest

class DontTestLaunchParams():
    def test_process_params(self):
        '''
        Should process parameters.
        '''
        for (key, val) in create_params_tp().iteritems():
            if not 'custom_' in key and not 'ext_' in key:
                self.assertEquals(self.tool.launch_params[key], val)

        # TODO: Test roles

        # TODO: Test params

    def test_custom_extension_parameters(self):
        '''
        Should handle custom/extension parameters.
        '''
        self.assertEquals(self.tool.get_custom_param('param1'), 'custom1')
        self.assertEquals(self.tool.get_custom_param('param2'), 'custom2')
        self.assertEquals(self.tool.get_ext_param('lti_message_type'),
                'extension-lti-launch')
        self.tool.set_custom_param('param3', 'custom3')
        self.tool.set_ext_param('user_id', 'bob')

        params = self.tool.to_params()
        self.assertEquals(params['custom_param1'], 'custom1')
        self.assertEquals(params['custom_param2'], 'custom2')
        self.assertEquals(params['custom_param3'], 'custom3')
        self.assertEquals(params['ext_lti_message_type'],
                'extension-lti-launch')
        self.assertEquals(params['ext_user_id'], 'bob')

    def test_invalid_request(self):
        '''
        Should not accept invalid request.
        '''
        # TODO: create request, and validate
        pass

        #request = Net::HTTP::Post.new('/test?key=value')
        #@tool.valid_request?(request).should == false

class TestProviderLaunchParams(unittest.TestCase, DontTestLaunchParams):
    '''
    Tests the LaunchParamsMixin component of the ToolProvider.
    '''
    def setUp(self):
        self.tool = create_test_tp()

class TestConsumerLaunchParams(unittest.TestCase, DontTestLaunchParams):
    '''
    Tests the LaunchParamsMixin component of the ToolConsumer.
    '''
    def setUp(self):
        self.tool = create_test_tc()
