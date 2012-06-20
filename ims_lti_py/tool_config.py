from collections import defaultdict

# Namespaces used for parsing configuration XML
LTI_NAMESPACES = {
        "xmlns": 'http://www.imsglobal.org/xsd/imslticc_v1p0',
        "blti": 'http://www.imsglobal.org/xsd/imsbasiclti_v1p0',
        "lticm": 'http://www.imsglobal.org/xsd/imslticm_v1p0',
        "lticp": 'http://www.imsglobal.org/xsd/imslticp_v1p0',
        }

class ToolConfig():
    '''
    Object used to represent LTI configuration.

    Capable of creating and reading the Common Cartridge XML representation of
    LTI links as described here:
        http://www.imsglobal.org/LTI/v1p1pd/ltiIMGv1p1pd.html#_Toc309649689

    TODO: Usage description
    '''
    def __init__(self, opts = defaultdict(lambda: None)):
        '''
        Create a new ToolConfig with the given options.
        '''
        self.custom_params = opts.pop('custom_params') or\
                defaultdict(lambda: None)
        self.extensions = opts.pop('extensions') or\
                defaultdict(lambda: None)
        self.opts = defaultdict(lambda: None)

        for (key, val) in opts.iteritems():
            self.opts[key] = val

    def create_from_xml(self):
        '''
        Create a ToolConfig from the given XML.
        '''
        # TODO: WTF!?
        pass

    def set_custom_param(self, key, val):
        '''
        Set a custom parameter to provided value.
        '''
        self.custom_params[key] = val

    def get_custom_param(self, key):
        '''
        Gets a custom parameter. It not yet set, returns None object.
        '''
        return self.custom_params[key]

    def set_ext_params(self, ext_key, ext_params):
        '''
        Set the extension parameters for a specific vendor.
        '''
        self.extensions[ext_key] = ext_params

    def get_ext_params(self, ext_key):
        '''
        Get extension paramaters for provided extension. It not set, returns None object.
        '''
        return self.extensions[ext_key]

    def set_ext_param(self, ext_key, param_key, val):
        '''
        Set the provided parameter in a set of extension parameters.
        '''
        if not self.extensions[ext_key]:
            self.extensions[ext_key] = defaultdict(lambda: None)
        self.extensions[ext_key][param_key] = val

    def get_ext_param(self, ext_key, param_key):
        '''
        Get specific param in set of provided extension parameters.
        '''
        return self.extensions[ext_key][param_key] if self.extensions[ext_key]\
                else None

    def process_xml(xml):
        '''
        Parse tool configuration data out of the Common Cartridge LTI link XML.
        '''
        # TODO Parse XML
        pass

    def to_xml(opts = defaultdict(lambda: None)):
        '''
        Generate XML from the current settings.
        '''
        # TODO Generte XML
        pass



