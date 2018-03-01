
from .launch_params import CONTENT_PARAMS_REQUIRED

from .tool_outbound import ToolOutbound

class ContentItemResponse(ToolOutbound):

    def has_required_params(self):
        return all([
            self.launch_params.get(x) for x in CONTENT_PARAMS_REQUIRED
        ])
