from test_helper import create_test_tp

import unittest

class TestOutcomeRequest(unittest.TestCase):
    def setUp(self):
        self.tp = create_test_tp()
        self.expected_xml = '<?xml version="1.0" encoding="UTF-8"?><imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/lis/oms1p0/pox"><imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>123456789</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody>%s</imsx_POXBody></imsx_POXEnvelopeRequest>'
        self.replace_result_xml = self.expected_xml %('<replaceResultRequest><resultRecord><sourcedGUID><sourcedId>261-154-728-17-784</sourcedId></sourcedGUID><result><resultScore><language>en</language><textString>5</textString></resultScore></result></resultRecord></replaceResultRequest>')
        self.read_result_xml = self.expected_xml %('<readResultRequest><resultRecord><sourcedGUID><sourcedId>261-154-728-17-784</sourcedId></sourcedGUID></resultRecord></readResultRequest>')
        self.delete_result_xml = self.expected_xml %('<deleteResultRequest><resultRecord><sourcedGUID><sourcedId>261-154-728-17-784</sourcedId></sourcedGUID></resultRecord></deleteResultRequest>')

    def mock_request(self, expected_xml):
        pass

    def test_post_replace_result(self):
        self.mock_request(self.replace_result_xml)
        self.tp.post_replace_result(5)

    # TODO
