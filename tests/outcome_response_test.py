from outcome_response import OutcomeResponse 

import unittest
import textwrap

class TestOutcomeResponse(unittest.TestCase):
    def setUp(self):
        self.response_xml = textwrap.dedent('''\
                <?xml version="1.0" encoding="UTF-8"?>
                <imsx_POXEnvelopeResponse xmlns="http://www.imsglobal.org/lis/oms1p0/pox">
                <imsx_POXHeader>
                <imsx_POXResponseHeaderInfo>
                <imsx_version>V1.0</imsx_version>
                <imsx_messageIdentifier></imsx_messageIdentifier>
                <imsx_statusInfo>
                <imsx_codeMajor>success</imsx_codeMajor>
                <imsx_severity>status</imsx_severity>
                <imsx_description></imsx_description>
                <imsx_messageRefIdentifier>123456789</imsx_messageRefIdentifier>
                <imsx_operationRefIdentifier>replaceResult</imsx_operationRefIdentifier>
                </imsx_statusInfo>
                </imsx_POXResponseHeaderInfo>
                </imsx_POXHeader>
                <imsx_POXBody>
                <replaceResultResponse></replaceResultResponse>
                </imsx_POXBody>
                </imsx_POXEnvelopeResponse>
                ''')

    def mock_response(self, response_xml):
        pass

    def test_parse_replace_result_response_xml(self):
        '''
        Should parse replaceResult response XML.
        '''
        result = OutcomeResponse()
        self.assertTrue(result.is_success())
        self.assertEqual(result.code_major, 'success')
        self.assertEqual(result.severity, 'status')
        self.assertEqual(result.description, None)
        self.assertEqual(result.message_ref_identifier, '123456789')
        self.assertEqual(result.operation, 'replaceResult')
        self.assertEqual(result.score, None)

    def test_parse_read_result_response_xml(self):
        '''
        Should parse readResult response XML.
        '''
        pass

    def test_parse_delete_result_response_xml(self):
        '''
        Should parse deleteResult response XML.
        '''
        result = OutcomeResponse()
        self.assertTrue(result.is_success())
        self.assertEqual(result.code_major, 'success')
        self.assertEqual(result.severity, 'status')
        self.assertEqual(result.description, None)
        self.assertEqual(result.message_ref_identifier, '123456789')
        self.assertEqual(result.operation, 'deleteResult')
        self.assertEqual(result.score, None)

    def test_recognize_failure_response(self):
        '''
        Should recognize a failure response.
        '''
        result = OutcomeResponse()
        self.assertTrue(result.is_failure())

    def test_generate_response_xml(self):
        '''
        Should generate response XML.
        '''
        result = OutcomeResponse()
        # TODO
