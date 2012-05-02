from launch_params import LaunchParamsMixin

class ToolConsumer(LaunchParamsMixin):
    def __init__(self, consumer_key, consumer_secret, params = {}):
        '''
        Create new ToolConsumer.
        '''
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.launch_url = params['launch_url']
        self.process_params(params)

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
        return self.consumer_key and self.consumer_secret and\
                self.resource_link_id and self.launch_url

    def generate_launch_data(self):
        pass

        # TODO: Validate params
        # TODO: Parse URL to get host
        # TODO: Get new OAuth consumer
        # TODO: Send request to launch URL
