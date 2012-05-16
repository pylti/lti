from test_helper import create_test_tp, create_test_tc, create_params_tp,\
        create_params_tc

import unittest

class TestProviderLaunchParams(unittest.testCase):
    '''
    Tests the LaunchParamsMixin component of the ToolProvider.
    '''
    def setUp(self):
        self.tp = create_test_tp()

    def test_process_params(self):
        '''
        Should process parameters.
        '''
        for (key, val) in create_test_tp().iteritems():
            if not 'custom_' in key and not 'ext_' in key:
                self.assertEqual(self.tp.launch_params['key'], val)

        # TODO: Test roles

        # TODO: Test params

      it "should handle custom/extension parameters" do
        @tool.get_custom_param('param1').should == 'custom1'
        @tool.get_custom_param('param2').should == 'custom2'
        @tool.get_ext_param('lti_message_type').should == 'extension-lti-launch'

        @tool.set_custom_param("param3", "custom3")
        @tool.set_ext_param("user_id", "bob")

        params = @tool.to_params
        params["custom_param1"].should == 'custom1'
        params["custom_param2"].should == 'custom2'
        params["custom_param3"].should == 'custom3'
        params["ext_lti_message_type"].should == "extension-lti-launch"
        params["ext_user_id"].should == "bob"
      end

      it "should not accept invalid request" do
        request = Net::HTTP::Post.new('/test?key=value')
        @tool.valid_request?(request).should == false
      end

class TestConsumerLaunchParams(unittest.testCase):
    '''
    Tests the LaunchParamsMixin component of the ToolConsumer.
    '''
    def setUp(self):
        self.tc = create_test_tc()

    def test_process_params(self):
        '''
        Should process parameters.
        '''
        # TODO
        pass
