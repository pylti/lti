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
        # Store specified options in our options member
        self.options = defaultdict(lambda: None)
        for (key, val) in opts.iteritems():
            self.options[key] = val

    @staticmethod
    def from_post_request(post_request):
        '''
        Convenience method for creating a new OutcomeRequest from a request
        object.

        post_request is assumed to be a Django HttpRequest object
        '''
        request = OutcomeRequest()
        request.options['post_request'] = post_request
        request.process_xml(post_request.POST)
        return request

    def post_replace_result(self, score):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult.
        '''
        self.options['operation'] = REPLACE_REQUEST
        self.options['score'] = score
        self.post_outcome_request()

    def post_delete_result(self):
        '''
        POSTs a deleteRequest to the Tool Consumer.
        '''
        self.options['operation'] = DELETE_REQUEST
        self.post_outcome_request()

    def post_read_result(self):
        '''
        POSTS a readResult to the Tool Consumer.
        '''
        self.options['operation'] = READ_REQUEST
        self.post_outcome_request()

    def is_replace_request(self):
        '''
        Check whether this request is a replaceResult request.
        '''
        return self.options['operation'] == REPLACE_REQUEST

    def is_delete_request(self):
        '''
        Check whether this request is a deleteResult request.
        '''
        return self.options['operation'] == DELETE_REQUEST

    def is_read_request(self):
        '''
        Check whether this request is a readResult request.
        '''
        return self.options['operation'] == READ_REQUEST

    def was_outcome_post_successful(self):
        return self.options['outcome_response'] and\
                self.options['outcome_response'].is_success()

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
