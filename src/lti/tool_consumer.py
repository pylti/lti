
from .launch_params import LAUNCH_PARAMS_REQUIRED

from .tool_outbound import ToolOutbound

class ToolConsumer(ToolOutbound):

    def has_required_params(self):
        return all([
            self.launch_params.get(x) for x in LAUNCH_PARAMS_REQUIRED
        ])

    def set_config(self, config):
        '''
        Set launch data from a ToolConfig.
        '''
        if self.launch_url is None:
            self.launch_url = config.launch_url
            self.launch_params.update(config.custom_params)
