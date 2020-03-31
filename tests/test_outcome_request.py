from lti.outcome_request import REPLACE_REQUEST
from lti import OutcomeRequest, OutcomeResponse, InvalidLTIConfigError

import unittest
from oauthlib.common import unquote
from httmock import all_requests, HTTMock
from django.conf import settings
from django.test import RequestFactory

settings.configure()

EXPECTED_XML = b'''<?xml version="1.0" encoding="UTF-8"?>
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

REPLACE_RESULT_XML = EXPECTED_XML[:] % b'''
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

READ_RESULT_XML = EXPECTED_XML[:] % b'''
<readResultRequest>
    <resultRecord>
        <sourcedGUID>
            <sourcedId>261-154-728-17-784</sourcedId>
        </sourcedGUID>
    </resultRecord>
</readResultRequest>
'''

DELETE_RESULT_XML = EXPECTED_XML[:] % b'''
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
        request_headers = {"User-Agent": "unit-test"}
        request = OutcomeRequest(headers=request_headers)
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
        self.assertEqual(request.headers.get('user-agent'), b"unit-test")
        self.assertEqual(request.headers.get('content-type'), b"application/xml")
        auth_header = unquote(request.headers['authorization'].decode('utf-8'))
        correct = ('OAuth '
            'oauth_nonce="my_nonce", oauth_timestamp="1234567890", '
            'oauth_version="1.0", oauth_signature_method="HMAC-SHA1", '
            'oauth_consumer_key="consumer", '
            'oauth_body_hash="glWvnsZZ8lMif1ATz8Tx64CTTaY=", '
            'oauth_signature="XR6A1CmUauXZdJZXa1pJpTQi6OQ="')
        self.assertEqual(auth_header, correct)

    def test_from_post_request(self):
        factory = RequestFactory()
        post_request = factory.post('/',
            data=REPLACE_RESULT_XML,
            content_type='application/xml'
        )
        request_headers = {"User-Agent": "post-request", "Content-Type": "text/xml"}
        request = OutcomeRequest.from_post_request(post_request, request_headers)
        self.assertEqual(request.operation, 'replaceResult')
        self.assertEqual(request.lis_result_sourcedid, '261-154-728-17-784')
        self.assertEqual(request.message_identifier, '123456789')
        self.assertEqual(request.score, '5')
        self.assertEqual(request.headers.get('User-Agent'), "post-request")
        self.assertEqual(request.headers.get('Content-Type'), "text/xml")
