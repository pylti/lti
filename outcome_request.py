from collections import defaultdict

REPLACE_REQUEST = 'replaceResult'
DELETE_REQUEST = 'deleteResult'
READ_REQUEST = 'readResult'

class OutcomeRequest():
    '''
    Class for consuming & generating LTI Outcome Requests.

    Outcome Request documentation: http://www.imsglobal.org/lti/v1p1pd/ltiIMGv1p1pd.html#_Toc309649691

    This class can be used both by Tool Providers and Tool Consumers, though
    they each use it differently. The TP will use it to POST an OAuth-signed
    request to the TC. A TC will use it to parse such a request from a TP.
    '''
    def __init__(self, opts = defaultdict(lambda: None)):
        self.options = defaultdict(lambda: None)
        for (key, val) in opts.iteritems():
            self.options[key] = val

    def from_post_request(post_request):
        '''
        Convenience method for creating a new OutcomeRequest from a request
        object.
        '''
        request = OutcomeRequest()
        request.post_request = post_request
        if post_request.body.read:
            xml = post_request.body.read
            post_request.body.rewind
        else:
            xml = post_request.body

        request.process_xml(xml)
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
        return self.outcome_response and self.outcome_response.success()

    def post_outcome_request(self):
        '''
        POST an OAuth signed request to the Tool Consumer.
        '''
        # TODO
        pass

    def process_xml(self):
        '''
        Parse Outcome Request data from XML.
        '''
        # TODO
        pass

    def has_required_attributes(self):
      self.consumer_key\
              and self.consumer_secret\
              and self.lis_outcome_service_url\
              and self.lis_result_sourcedid\
              and self.operation

    def generate_request_xml(self):
        # TODO
        pass
