from launch_params import LaunchParams

class ToolProvider(LaunchParams):
    '''
    Implements the LTI Tool Provider.
    '''
    
    def __init__(self, consumer_key, consumer_secret, params = {}):
        '''
        Create new ToolProvider.
        '''
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.custom_params = {}
        self.ext_params = {}
        self.non_spec_params = {}
        self.outcome_requests = []
        self.process_params(params)

    def has_role(self, role):
        '''
        Check whether the Launch Paramters set the role.
        '''
        return self.roles and role in self.roles

    def is_student(self):
        '''
        Convenience method for checking if the user has 'learner' or 'student'
        role.
        '''
        return self.has_role('learner') or self.has_role('student')

    def is_instructor(self):
        '''
        Convenience method for checking if user has 'instructor', 'faculty'
        or 'staff' role.
        '''
        return self.has_role('instructor') or self.has_role('faculty') or\
                self.has_role('staff')

    def launch_request(self):
        '''
        Check if the request was an LTI Launch Request.
        '''
        return self.lti_message_type == 'basic-lti-launch-request'

    def outcome_service(self):
        '''
        Check if the Tool Launch expects an Outcome Result.
        '''
        return (self.lis_outcome_service_url and self.lis_result_sourcedid)

    def username(self, default = None):
        '''
        Return the full, given, or family name if set.
        '''
        if self.lis_person_name_given:
            return self.lis_person_name_given
        elif self.lis_person_name_family:
            return self.lis_person_name_family
        elif self.lis_person_name_full:
            return self.lis_person_name_full
        else:
            return default

    def post_replace_result(self, score):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult.

        Returns OutcomeResponse object and stores it in self.outcome_request
        '''
        return self.new_request.post_replace_result(score)

    def post_delete_result(self):
        '''
        POSTs a delete request to the Tool Consumer.
        '''
        return self.new_request.post_delet_result()

    def post_read_result(self):
        '''
        POSTs the given score to the Tool Consumer with a replaceResult, the
        returned OutcomeResponse will have the score.
        '''
        return self.new_request.post_read_result()

    def last_outcome_request(self):
        return self.outcome_requests.last

    def build_return_url(self):
        '''
        If the Tool Consumer sent a return URL, add any set messages to the
        URL.
        '''
        if not self.launch_presentation_return_url:
            return None

        messages = []
        for message in ['lti_errormsg', 'lti_errorlog', 'lti_msg', 'lti_log']:
            # TODO: Implement
            #if message == self.
            pass
        
    def new_request(self):
        # TODO: Implement OutcomeRequest 
        pass
