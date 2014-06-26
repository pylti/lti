from test_helper import create_test_tp
from ims_lti_py import OutcomeRequest

import unittest
import oauth2

class MockResponse(object):
    def __init__(self):
        self.status = '200'
        self.data = '<xml/>'

# Fake OAuth requests
def stubify(arg0, arg1, method = None, body = None, headers = None):
    return (MockResponse(), '<xml/>')
oauth2.Client.request = stubify

class TestOutcomeRequest(unittest.TestCase):
    def setUp(self):
        self.tp = create_test_tp()
        self.expected_xml = '<?xml version="1.0" encoding="UTF-8"?><imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/lis/oms1p0/pox"><imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>123456789</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody>%s</imsx_POXBody></imsx_POXEnvelopeRequest>'
        self.replace_result_xml = self.expected_xml[:] %('<replaceResultRequest><resultRecord><sourcedGUID><sourcedId>261-154-728-17-784</sourcedId></sourcedGUID><result><resultScore><language>en</language><textString>5</textString></resultScore></result></resultRecord></replaceResultRequest>')
        self.read_result_xml = self.expected_xml[:] %('<readResultRequest><resultRecord><sourcedGUID><sourcedId>261-154-728-17-784</sourcedId></sourcedGUID></resultRecord></readResultRequest>')
        self.delete_result_xml = self.expected_xml[:] %('<deleteResultRequest><resultRecord><sourcedGUID><sourcedId>261-154-728-17-784</sourcedId></sourcedGUID></resultRecord></deleteResultRequest>')
         
    def test_post_replace_result(self):
        '''
        Should post replaceResult rquest.
        '''
        self.tp.post_replace_result(5)
        self.assertFalse(self.tp.last_outcome_success())

    def test_post_read_result(self):
        '''
        Should post readResult request.
        '''
        self.tp.post_read_result()

    def  test_post_delete_result(self):
        '''
        Should post deleteResult request.
        '''
        self.tp.post_delete_result()

    def test_parse_replace_result_xml(self):
        '''
        Should parse replaceResult XML.
        '''
        request = OutcomeRequest()
        request.process_xml(self.replace_result_xml)
        self.assertEqual(request.operation, 'replaceResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, '5')

    def test_parse_read_result_xml(self):
        '''
        Should parse readResult XML.
        '''
        request = OutcomeRequest()
        request.process_xml(self.read_result_xml)
        self.assertEqual(request.operation, 'readResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, None)

    def test_parse_delete_result_xml(self):
        '''
        Should parse deleteRequest XML.
        '''
        request = OutcomeRequest()
        request.process_xml(self.delete_result_xml)
        self.assertEqual(request.operation, 'deleteResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, None)
