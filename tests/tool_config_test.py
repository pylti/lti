from ims_lti_py import ToolConfig, InvalidLTIConfigError

import unittest

cc_lti_xml = '<?xml version="1.0" encoding="UTF-8"?><cartridge_basiclti_link xmlns:lticm="http://www.imsglobal.org/xsd/imslticm_v1p0" xmlns:blti="http://www.imsglobal.org/xsd/imsbasiclti_v1p0" xmlns:lticp="http://www.imsglobal.org/xsd/imslticp_v1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imslticc_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticc_v1p0.xsd http://www.imsglobal.org/xsd/imsbasiclti_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imsbasiclti_v1p0p1.xsd http://www.imsglobal.org/xsd/imslticm_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticm_v1p0.xsd http://www.imsglobal.org/xsd/imslticp_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticp_v1p0.xsd" xmlns="http://www.imsglobal.org/xsd/imslticc_v1p0"><blti:title>Test Config</blti:title><blti:description>Description of boringness</blti:description><blti:launch_url>http://www.example.com/lti</blti:launch_url><blti:secure_launch_url>https://www.example.com/lti</blti:secure_launch_url><blti:vendor><lticp:name>test.tool</lticp:name><lticp:code>test</lticp:code><lticp:description>We test things</lticp:description><lticp:url>http://www.example.com/about</lticp:url><lticp:contact><lticp:name>Joe Support</lticp:name><lticp:email>support@example.com</lticp:email></lticp:contact></blti:vendor><blti:custom><lticm:property name="custom1">customval1</lticm:property><lticm:property name="custom2">customval2</lticm:property></blti:custom><blti:extensions platform="example.com"><lticm:property name="extkey1">extval1</lticm:property><lticm:options name="extopt1"><lticm:property name="optkey2">optval2</lticm:property><lticm:property name="optkey1">optval1</lticm:property></lticm:options><lticm:property name="extkey2">extval2</lticm:property></blti:extensions><blti:extensions platform="two.example.com"><lticm:property name="ext1key">ext1val</lticm:property></blti:extensions><cartridge_bundle identifierref="BLTI001_Bundle"/></cartridge_basiclti_link>'

class TestToolConfig(unittest.TestCase):
    def test_generate_xml(self):
        '''
        Should generate the expected config xml.
        '''
        config = ToolConfig(title = "Test Config", 
                secure_launch_url = "https://www.example.com/lti", 
                custom_params = {"custom1": "customval1"})
        config.description ='Description of boringness'
        config.launch_url = 'http://www.example.com/lti'
        config.icon = 'http://wil.to/_/beardslap.gif'
        config.vendor_code = 'test'
        config.vendor_name = 'test.tool'
        config.vendor_description = 'We test things'
        config.vendor_url = 'http://www.example.com/about'
        config.vendor_contact_email = 'support@example.com'
        config.vendor_contact_name = 'Joe Support'

        config.set_custom_param('custom2', 'customval2')

        config.set_ext_params('example.com', { 'extkey1': 'extval1' })
        config.set_ext_param('example.com', 'extkey2', 'extval2')
        config.set_ext_param('example.com', 'extopt1', 
                { 'optkey1': 'optval1', 'optkey2': 'optval2' })
        config.set_ext_param('two.example.com', 'ext1key', 'ext1val')

        config.cartridge_bundle = 'BLTI001_Bundle'

        xml = config.to_xml()
        self.assertEqual(xml, cc_lti_xml)

    def test_read_xml_config(self):
        '''
        Should read an XML config.
        '''
        config = ToolConfig.create_from_xml(cc_lti_xml)
        self.assertEqual(config.to_xml(), cc_lti_xml)

    def test_invalid_config_xml(self):
        '''
        Should not allow creating invalid config xml.
        '''
        config = ToolConfig(title = 'Test Config')
        self.assertRaises(InvalidLTIConfigError, config.to_xml)
