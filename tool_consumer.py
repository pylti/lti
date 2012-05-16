from launch_params import LaunchParamsMixin
from request_validator import RequestValidatorMixin
from collections import defaultdict

class ToolConsumer(LaunchParamsMixin, RequestValidatorMixin, object):
    def __init__(self, consumer_key, consumer_secret, params =
            defaultdict(lambda: None)):
        '''
        Create new ToolConsumer.
        '''
        super(ToolConsumer, self).__init__()

        # Prevent key errors
        params_dict = defaultdict(lambda: None)
        params_dict.update(params)

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.launch_url = params_dict['launch_url']
        self.process_params(params_dict)

    def set_config(self, config):
        '''
        Set launch data from a ToolConfig.
        '''
        # TODO: Implement ToolConfig
        pass

    def has_required_params(self):
        '''
        Check if required parameters for a tool launch are set.
        '''
        return self.consumer_key and\
                self.consumer_secret and\
                self.launch_params['resource_link_id'] and\
                self.launch_url

    def generate_launch_data(self):
        pass

        # TODO: Validate params
        # TODO: Parse URL to get host
        # TODO: Get new OAuth consumer
        # TODO: Send request to launch URL
