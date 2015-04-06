from ims_lti_py.outcome_request import REPLACE_REQUEST
from ims_lti_py import OutcomeRequest, OutcomeResponse, InvalidLTIConfigError

import unittest
from oauthlib.common import unquote
from httmock import all_requests, HTTMock

EXPECTED_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">
    <imsx_POXHeader>
        <imsx_POXRequestHeaderInfo>
            <imsx_version>V1.0</imsx_version>
            <imsx_messageIdentifier>123456789</imsx_messageIdentifier>
        </imsx_POXRequestHeaderInfo>
    </imsx_POXHeader>
    <imsx_POXBody>
    %s
    </imsx_POXBody>
</imsx_POXEnvelopeRequest>
'''

REPLACE_RESULT_XML = EXPECTED_XML[:] % '''
<replaceResultRequest>
    <resultRecord>
        <sourcedGUID>
            <sourcedId>261-154-728-17-784</sourcedId>
        </sourcedGUID>
        <result>
            <resultScore>
                <language>en</language>
                <textString>5</textString>
            </resultScore>
        </result>
    </resultRecord>
</replaceResultRequest>
'''

READ_RESULT_XML = EXPECTED_XML[:] % '''
<readResultRequest>
    <resultRecord>
        <sourcedGUID>
            <sourcedId>261-154-728-17-784</sourcedId>
        </sourcedGUID>
    </resultRecord>
</readResultRequest>
'''

DELETE_RESULT_XML = EXPECTED_XML[:] % '''
<deleteResultRequest>
    <resultRecord>
        <sourcedGUID>
            <sourcedId>261-154-728-17-784</sourcedId>
        </sourcedGUID>
    </resultRecord>
</deleteResultRequest>
'''

@all_requests
def response_content(url, request):
    return {'status_code': 200,
            'content': 'Oh hai'}

class TestOutcomeRequest(unittest.TestCase):

    def test_parse_replace_result_xml(self):
        '''
        Should parse replaceResult XML.
        '''
        request = OutcomeRequest()
        request.process_xml(REPLACE_RESULT_XML)
        self.assertEqual(request.operation, 'replaceResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, '5')

    def test_parse_read_result_xml(self):
        '''
        Should parse readResult XML.
        '''
        request = OutcomeRequest()
        request.process_xml(READ_RESULT_XML)
        self.assertEqual(request.operation, 'readResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, None)

    def test_parse_delete_result_xml(self):
        '''
        Should parse deleteRequest XML.
        '''
        request = OutcomeRequest()
        request.process_xml(DELETE_RESULT_XML)
        self.assertEqual(request.operation, 'deleteResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, None)

    def test_has_required_attributes(self):
        request = OutcomeRequest()
        self.assertFalse(request.has_required_attributes())
        request.consumer_key = 'foo'
        request.consumer_secret = 'bar'
        self.assertFalse(request.has_required_attributes())
        request.lis_outcome_service_url = 'http://example.edu/'
        request.lis_result_sourcedid = 1
        request.operation = 'baz'
        self.assertTrue(request.has_required_attributes())

    def test_post_outcome_request(self):
        request = OutcomeRequest()
        self.assertRaises(InvalidLTIConfigError, request.post_outcome_request)
        request.consumer_key = 'consumer'
        request.consumer_secret = 'secret'
        request.lis_outcome_service_url = 'http://example.edu/'
        request.lis_result_sourcedid = 'foo'
        request.operation = REPLACE_REQUEST
        with HTTMock(response_content):
            resp = request.post_outcome_request(
                nonce='my_nonce',
                timestamp='1234567890'
            )
        self.assertIsInstance(resp, OutcomeResponse)
        request = resp.post_response.request
        self.assertTrue('authorization' in request.headers)
        auth_header = unquote(request.headers['authorization'])
        correct = ('OAuth '
            'oauth_nonce="my_nonce", oauth_timestamp="1234567890", '
            'oauth_version="1.0", oauth_signature_method="HMAC-SHA1", '
            'oauth_consumer_key="consumer", '
            'oauth_signature="rbvjzAHwXPs/e41Runtu6w9Gv+w="')
        self.assertEqual(auth_header, correct)

