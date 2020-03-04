from collections import defaultdict
from lxml import etree
from lxml import objectify

from lxml.etree import QName

from .utils import InvalidLTIConfigError

VALID_ATTRIBUTES = [
    'title',
    'description',
    'launch_url',
    'secure_launch_url',
    'icon',
    'secure_icon',
    'cartridge_bundle',
    'cartridge_icon',
    'vendor_code',
    'vendor_name',
    'vendor_description',
    'vendor_url',
    'vendor_contact_email',
    'vendor_contact_name'
]

NSMAP = {
    'blti': 'http://www.imsglobal.org/xsd/imsbasiclti_v1p0',
    'lticm': 'http://www.imsglobal.org/xsd/imslticm_v1p0',
    'lticp': 'http://www.imsglobal.org/xsd/imslticp_v1p0',
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
}


class ToolConfig(object):
    '''
    Object used to represent LTI configuration.

    Capable of creating and reading the Common Cartridge XML representation of
    LTI links as described here:
        http://www.imsglobal.org/LTI/v1p1/ltiIMGv1p1.html#_Toc319560470

    TODO: Usage description
    '''
    def __init__(self, **kwargs):
        '''
        Create a new ToolConfig with the given options.
        '''
        # Initialize all class accessors to None
        for attr in VALID_ATTRIBUTES:
            setattr(self, attr, None)

        for attr in ['custom_params', 'extensions']:
            if attr in kwargs:
                attr_val = kwargs.pop(attr)
            else:
                attr_val = defaultdict(lambda: None)
            setattr(self, attr, attr_val)

        # Iterate over all provided options and save to class instance members
        for (key, val) in kwargs.items():
            if key in VALID_ATTRIBUTES:
                setattr(self, key, val)
            else:
                raise InvalidLTIConfigError(
                    "Invalid outcome request option: {}".format(key)
                )

    @staticmethod
    def create_from_xml(xml):
        '''
        Create a ToolConfig from the given XML.
        '''
        config = ToolConfig()
        config.process_xml(xml)
        return config

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
        self.extensions.setdefault(ext_key, defaultdict(lambda: None))
        self.extensions[ext_key][param_key] = val

    def get_ext_param(self, ext_key, param_key):
        '''
        Get specific param in set of provided extension parameters.
        '''
        if ext_key in self.extensions:
            return self.extensions[ext_key].get(param_key)

    def process_xml(self, xml):
        '''
        Parse tool configuration data out of the Common Cartridge LTI link XML.
        '''
        root = objectify.fromstring(xml, parser=etree.XMLParser())
        # Parse all children of the root node
        for child in root.getchildren():
            if QName(child).localname == 'title':
                self.title = child.text
            if QName(child).localname == 'description':
                self.description = child.text
            if QName(child).localname == 'secure_launch_url':
                self.secure_launch_url = child.text
            if QName(child).localname == 'launch_url':
                self.launch_url = child.text
            if QName(child).localname == 'icon':
                self.icon = child.text
            if QName(child).localname == 'secure_icon':
                self.secure_icon = child.text
            if QName(child).localname == 'cartridge_bundle':
                self.cartridge_bundle = child.attrib['identifierref']
            if QName(child).localname == 'cartridge_icon':
                self.cartridge_icon = child.attrib['identifierref']

            if QName(child).localname == 'vendor':
                # Parse vendor tag
                for v_child in child.getchildren():
                    if QName(v_child).localname == 'code':
                        self.vendor_code = v_child.text
                    if QName(v_child).localname == 'description':
                        self.vendor_description = v_child.text
                    if QName(v_child).localname == 'name':
                        self.vendor_name = v_child.text
                    if QName(v_child).localname == 'url':
                        self.vendor_url = v_child.text
                    if QName(v_child).localname == 'contact':
                        # Parse contact tag for email and name
                        for c_child in v_child:
                            if QName(c_child).localname == 'name':
                                self.vendor_contact_name = c_child.text
                            if QName(c_child).localname == 'email':
                                self.vendor_contact_email = c_child.text

            if QName(child).localname == 'custom':
                # Parse custom tags
                for custom_child in child.getchildren():
                    self.custom_params[custom_child.attrib['name']] =\
                            custom_child.text

            if QName(child).localname == 'extensions':
                platform = child.attrib['platform']
                properties = {}

                # Parse extension tags
                for ext_child in child.getchildren():
                    if QName(ext_child).localname == 'property':
                        properties[ext_child.attrib['name']] = ext_child.text
                    elif QName(ext_child).localname == 'options':
                        opt_name = ext_child.attrib['name']
                        options = {}
                        for option_child in ext_child.getchildren():
                            options[option_child.attrib['name']] =\
                                    option_child.text
                        properties[opt_name] = options

                self.set_ext_params(platform, properties)

    def recursive_options(self, element, params):
        for key, val in sorted(params.items()):
            if isinstance(val, dict):
                options_node = etree.SubElement(
                    element,
                    '{%s}%s' % (NSMAP['lticm'], 'options'),
                    name=key,
                )
                for key, val in sorted(val.items()):
                    self.recursive_options(options_node, {key: val})
            else:
                param_node = etree.SubElement(
                    element,
                    '{%s}%s' % (NSMAP['lticm'], 'property'),
                    name=key,
                )
                param_node.text = val

    def to_xml(self, opts=defaultdict(lambda: None)):
        '''
        Generate XML from the current settings.
        '''
        if not self.launch_url or not self.secure_launch_url:
            raise InvalidLTIConfigError('Invalid LTI configuration')

        root = etree.Element(
            'cartridge_basiclti_link',
            attrib={
                '{%s}%s' % (NSMAP['xsi'], 'schemaLocation'): 'http://www.imsglobal.org/xsd/imslticc_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticc_v1p0.xsd http://www.imsglobal.org/xsd/imsbasiclti_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imsbasiclti_v1p0p1.xsd http://www.imsglobal.org/xsd/imslticm_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticm_v1p0.xsd http://www.imsglobal.org/xsd/imslticp_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticp_v1p0.xsd',
                'xmlns': 'http://www.imsglobal.org/xsd/imslticc_v1p0',
            },
            nsmap=NSMAP,
        )

        for key in ['title', 'description', 'launch_url', 'secure_launch_url']:
            option = etree.SubElement(root, '{%s}%s' % (NSMAP['blti'], key))
            option.text = getattr(self, key)

        if getattr(self, 'icon'):
            option = etree.SubElement(root, '{%s}%s' % (NSMAP['blti'], 'icon'))
            option.text = getattr(self, 'icon')

        if getattr(self, 'secure_icon'):
            option = etree.SubElement(root, '{%s}%s' % (NSMAP['blti'], 'secure_icon'))
            option.text = getattr(self, 'secure_icon')

        vendor_keys = ['name', 'code', 'description', 'url']
        if any('vendor_' + key for key in vendor_keys) or\
                self.vendor_contact_email:
                    vendor_node = etree.SubElement(
                        root,
                        '{%s}%s' % (NSMAP['blti'], 'vendor'),
                    )
                    for key in vendor_keys:
                        if getattr(self, 'vendor_' + key) is not None:
                            v_node = etree.SubElement(
                                vendor_node,
                                '{%s}%s' % (NSMAP['lticp'], key),
                            )
                            v_node.text = getattr(self, 'vendor_' + key)
                    if getattr(self, 'vendor_contact_email'):
                        v_node = etree.SubElement(
                            vendor_node,
                            '{%s}%s' % (NSMAP['lticp'], 'contact'),
                        )
                        c_name = etree.SubElement(
                            v_node,
                            '{%s}%s' % (NSMAP['lticp'], 'name'),
                        )
                        c_name.text = self.vendor_contact_name
                        c_email = etree.SubElement(
                            v_node,
                            '{%s}%s' % (NSMAP['lticp'], 'email'),
                        )
                        c_email.text = self.vendor_contact_email

        # Custom params
        if len(self.custom_params) != 0:
            custom_node = etree.SubElement(
                root,
                '{%s}%s' % (NSMAP['blti'], 'custom'),
            )
            for (key, val) in sorted(self.custom_params.items()):
                c_node = etree.SubElement(
                    custom_node,
                    '{%s}%s' % (NSMAP['lticm'], 'property'),
                )
                c_node.set('name', key)
                c_node.text = val

        # Extension params
        if len(self.extensions) != 0:
            for (key, params) in sorted(self.extensions.items()):
                extension_node = etree.SubElement(
                    root,
                    '{%s}%s' % (NSMAP['blti'], 'extensions'),
                    platform=key,
                )
                self.recursive_options(extension_node, params)

        if getattr(self, 'cartridge_bundle'):
            identifierref = etree.SubElement(
                root,
                'cartridge_bundle',
                identifierref=self.cartridge_bundle,
            )

        if getattr(self, 'cartridge_icon'):
            identifierref = etree.SubElement(
                root,
                'cartridge_icon',
                identifierref=self.cartridge_icon,
            )

        declaration = b'<?xml version="1.0" encoding="UTF-8"?>'
        return declaration + etree.tostring(root, encoding='utf-8')
