from collections import defaultdict
CODE_MAJOR_CODES = [
        'success',
        'processing',
        'failure',
        'unsupported'
]

SEVERITY_CODES = [
        'status',
        'warning',
        'error'
]

class OutcomeResponse():
    '''
    This class consumes & generates LTI Outcome Responses.
  
    Response documentation: http://www.imsglobal.org/lti/v1p1pd/ltiIMGv1p1pd.html#_Toc309649691

    Error code documentation: http://www.imsglobal.org/gws/gwsv1p0/imsgws_baseProfv1p0.html#1639667

    This class can be used by both Tool Providers and Tool Consumers, though
    each will use it differently. TPs will use it to partse the result of an
    OutcomeRequest to the TC. A TC will use it to generate proper response XML
    to send back to a TP.
    ''' 
    def __init__(self, opts = defaultdict(lambda: None)):
        # Store specified options in our options member
        for (key, val) in opts.iteritems():
            self.options[key] = val

    def from_post_response(self, post_response):
        '''
        Convenience method for creating a new OutcomeResponse from a response
        object.
        '''
        response = OutcomeResponse()
        response.post_response = post_response
        response.reponse_code = post_response.code
        xml = post_response.body
        response.process_xml(xml)
        return response

    def is_success(self):
        return self.code_major == 'success'

    def is_processing(self):
        return self.code_major == 'processing'

    def is_failure(self):
        return self.code_major == 'failure'

    def is_unsupported(self):
        return self.code_major == 'unsupported'

    def has_warning(self):
        return self.severity == 'warning'

    def has_error(self):
        return self.severity == 'error'

    def process_xml(xml):
        '''
        Parse OutcomeResponse data form XML.
        '''
        # TODO
        pass

    def generate_response_xml(self):
        '''
        Generate XML based on the current configuration.
        '''
        # TODO
        pass
