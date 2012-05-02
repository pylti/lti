class ToolConfig():
    '''
    Object used to represent LTI configuration.

    Capable of creating and reading the Common Cartridge XML representation of
    LTI links as described here:
        http://www.imsglobal.org/LTI/v1p1pd/ltiIMGv1p1pd.html#_Toc309649689

    TODO: Usage description
    '''
    def __init__(self, opts = {}):
        '''
        Create a new ToolConfig with the given options.
        '''
        self.custom_params = opts.pop('custom_params') or {}
        self.extensions = opts.pop('extensions') or {}

        for opt in opts:
            self.
