from ims_lti_py import OutcomeResponse 

import unittest

class TestOutcomeResponse(unittest.TestCase):
    def setUp(self):
        self.response_xml = '<?xml version="1.0" encoding="UTF-8"?><imsx_POXEnvelopeResponse xmlns="http://www.imsglobal.org/lis/oms1p0/pox"><imsx_POXHeader><imsx_POXResponseHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier></imsx_messageIdentifier><imsx_statusInfo><imsx_codeMajor>success</imsx_codeMajor><imsx_severity>status</imsx_severity><imsx_description></imsx_description><imsx_messageRefIdentifier>123456789</imsx_messageRefIdentifier><imsx_operationRefIdentifier>replaceResult</imsx_operationRefIdentifier></imsx_statusInfo></imsx_POXResponseHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultResponse/></imsx_POXBody></imsx_POXEnvelopeResponse>'

    def mock_response(self, response_xml):
        class mock_resp():
            def __init__(self):
                self.status_code = '200'
                self.data = response_xml

        return mock_resp()

    def test_parse_replace_result_response_xml(self):
        '''
        Should parse replaceResult response XML.
        '''
        fake = self.mock_response(self.response_xml)
        response = OutcomeResponse.from_post_response(fake)
        self.assertTrue(response.is_success())
        self.assertEqual(response.code_major, 'success')
        self.assertEqual(response.severity, 'status')
        self.assertEqual(response.description, '')
        self.assertEqual(response.message_ref_identifier, '123456789')
        self.assertEqual(response.operation, 'replaceResult')
        self.assertEqual(response.score, None)

    def test_parse_read_result_response_xml(self):
        '''
        Should parse readResult response XML.
        '''
        read_xml = self.response_xml.replace(\
                '<replaceResultResponse/>',\
                '''<readResultResponse>
<result>
<resultScore>
<language>en</language>
<textString>0.91</textString>
</resultScore>
</result>
</readResultResponse>''')
        fake = self.mock_response(read_xml)
        response = OutcomeResponse.from_post_response(fake)
        self.assertTrue(response.is_success())
        self.assertEqual(response.code_major, 'success')
        self.assertEqual(response.severity, 'status')
        self.assertEqual(response.description, '')
        self.assertEqual(response.message_ref_identifier, '123456789')
        self.assertEqual(response.score, '0.91')

    def test_parse_delete_result_response_xml(self):
        '''
        Should parse deleteResult response XML.
        '''
        delete_xml = self.response_xml.replace('replaceResult', 'deleteResult')
        fake = self.mock_response(delete_xml)
        result = OutcomeResponse.from_post_response(fake)
        self.assertTrue(result.is_success())
        self.assertEqual(result.code_major, 'success')
        self.assertEqual(result.severity, 'status')
        self.assertEqual(result.description, '')
        self.assertEqual(result.message_ref_identifier, '123456789')
        self.assertEqual(result.operation, 'deleteResult')
        self.assertEqual(result.score, None)

    def test_recognize_failure_response(self):
        '''
        Should recognize a failure response.
        '''
        failure_xml = self.response_xml.replace('success', 'failure')
        fake = self.mock_response(failure_xml)
        result = OutcomeResponse.from_post_response(fake)
        self.assertTrue(result.is_failure())

    def test_generate_response_xml(self):
        '''
        Should generate response XML.
        '''
        response = OutcomeResponse()
        response.process_xml(self.response_xml)
        self.assertEqual(response.generate_response_xml(), self.response_xml)
