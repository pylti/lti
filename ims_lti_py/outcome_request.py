from collections import defaultdict
from lxml import etree, objectify

import oauth2
import textwrap

from outcome_response import OutcomeResponse
from utils import InvalidLTIConfigError

REPLACE_REQUEST = 'replaceResult'
DELETE_REQUEST = 'deleteResult'
READ_REQUEST = 'readResult'

accessors = [
    'operation',
    'score',
    'outcome_response',
    'message_identifier',
    'lis_outcome_service_url',
    'lis_result_sourcedid',
    'consumer_key',
    'consumer_secret',
    'post_request'
]

class OutcomeRequest():
    '''
    Class for consuming & generating LTI Outcome Requests.

    Outcome Request documentation: http://www.imsglobal.org/lti/v1p1pd/ltiIMGv1p1pd.html#_Toc309649691

    This class can be used both by Tool Providers and Tool Consumers, though
    they each use it differently. The TP will use it to POST an OAuth-signed
    request to the TC. A TC will use it to parse such a request from a TP.
    '''
    def __init__(self, opts = defaultdict(lambda: None)):
        # Initialize all our accessors to None
        for accessor in accessors:
            setattr(self, accessor, None)

        # Store specified options in our accessors 
        for (key, val) in opts.iteritems():
            setattr(self, key, val)

    @staticmethod
    def from_post_request(post_request):
        '''
        Convenience method for creating a new OutcomeRequest from a request
        object.

        post_request is assumed to be a Django HttpRequest object
        '''
        request = OutcomeRequest()
        request.post_request = post_request
        request.process_xml(post_request.data)
        return request

    def post_replace_result(self, score):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult.
        '''
        self.operation = REPLACE_REQUEST
        self.score = score
        self.post_outcome_request()

    def post_delete_result(self):
        '''
        POSTs a deleteRequest to the Tool Consumer.
        '''
        self.operation = DELETE_REQUEST
        self.post_outcome_request()

    def post_read_result(self):
        '''
        POSTS a readResult to the Tool Consumer.
        '''
        self.operation = READ_REQUEST
        self.post_outcome_request()

    def is_replace_request(self):
        '''
        Check whether this request is a replaceResult request.
        '''
        return self.operation == REPLACE_REQUEST

    def is_delete_request(self):
        '''
        Check whether this request is a deleteResult request.
        '''
        return self.operation == DELETE_REQUEST

    def is_read_request(self):
        '''
        Check whether this request is a readResult request.
        '''
        return self.operation == READ_REQUEST

    def was_outcome_post_successful(self):
        return self.outcome_response and\
                self.outcome_response.is_success()

    def post_outcome_request(self):
        '''
        POST an OAuth signed request to the Tool Consumer.
        '''
        if not self.has_required_attributes():
            raise InvalidLTIConfigError('OutcomeRequest does not have all required attributes')

        consumer = oauth2.Consumer(key = self.consumer_key,
                secret =  self.consumer_secret)

        client = oauth2.Client(consumer)

        response, content = client.request(
                self.lis_outcome_service_url,
                'POST',
                body = self.generate_request_xml(),
                headers = { 'Content-Type': 'application/xml' })

        self.outcome_response =OutcomeResponse.from_post_response(response)

    def process_xml(self, xml):
        '''
        Parse Outcome Request data from XML.
        '''
        root = objectify.fromstring(xml)
        import ipdb; ipdb.set_trace()
        self.message_identifier = root.imsx_POXHeader.\
                imsx_POXRequestHeaderInfo.imsx_messageIdentifier
        try:
            self.operation = REPLACE_REQUEST
            result = root.imsx_POXBody.replaceResultRequest
            self.lis_result_sourcedid = result.resultRecord.\
                    sourceGUID.sourcedId
        except:
            pass

        try:
            result = root.imsx_POXBody.deleteResultRequest
        except:
            pass

        try:
            result = root.imsx_POXBody.readResultRequest
        except:
            pass

    def has_required_attributes(self):
        return self.consumer_key != None\
                and self.consumer_secret != None\
                and self.lis_outcome_service_url != None\
                and self.lis_result_sourcedid != None\
                and self.operation != None

    def generate_request_xml(self):
        root = etree.Element('imsx_POXEnvelopeResponse', xmlns =
                'http://www.imsglobal.org/lis/oms1p0/pox')

        header = etree.SubElement(root, 'imsx_POXHeader')
        header_info = etree.SubElement(header, 'imsx_POXResponseHeaderInfo')
        version = etree.SubElement(header_info, 'imsx_version')
        version.text = 'V1.0'
        message_identifier = etree.SubElement(header_info,
                'imsx_messageIdentifier')
        message_identifier.text = self.message_identifier
        body = etree.SubElement(root, 'imsx_POXBody')
        request = etree.SubElement(body, '%s%s' %(self.operation,
            'Request'))
        record = etree.SubElement(request, 'resultRecord')
        guid = etree.SubElement(record, 'sourcedId')
        guid.text = self.lis_result_sourcedid
        
        if self.score:
            result = etree.SubElement(record, 'result')
            result_score = etree.SubElement(result, 'resultScore')
            language = etree.SubElement(result_score, 'language')
            language.text = 'en'
            text_string = etree.SubElement(result_score, 'textString')
            text_string.text = self.score.__str__()

        return etree.tostring(root, xml_declaration = True, encoding = 'utf-8')
