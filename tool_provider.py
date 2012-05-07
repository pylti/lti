from collections import defaultdict
from launch_params import LaunchParamsMixin
from urllib import quote

class ToolProvider(LaunchParamsMixin, object):
    '''
    Implements the LTI Tool Provider.
    '''
    
    def __init__(self, consumer_key, consumer_secret, params = {}):
        '''
        Create new ToolProvider.
        '''
        super(ToolProvider, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.non_spec_params = defaultdict(lambda: None)
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

    def is_launch_request(self):
        '''
        Check if the request was an LTI Launch Request.
        '''
        return self.launch_params['lti_message_type'] ==\
                'basic-lti-launch-request'

    def is_outcome_service(self):
        '''
        Check if the Tool Launch expects an Outcome Result.
        '''
        return (self.launch_params['lis_outcome_service_url']and
                self.launch_params['lis_result_sourcedid'])

    def username(self, default = None):
        '''
        Return the full, given, or family name if set.
        '''
        if self.launch_params['lis_person_name_given']:
            return self.launch_params['lis_person_name_given']
        elif self.launch_params['lis_person_name_family']:
            return self.launch_params['lis_person_name_family']
        elif self.launch_params['lis_person_name_full']:
            return self.launch_params['lis_person_name_full']
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
        return self.new_request.post_delete_result()

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
        if not self.launch_params['launch_presentation_return_url']:
            return None

        messages = []
        for message in ['lti_errormsg', 'lti_errorlog', 'lti_msg', 'lti_log']:
            if self.launch_params[message]:
                messages.append('%s=%s' %(message,
                    quote(self.launch_params[message])))

        q_string = '?' + '&'.join(messages) if messages else ''
        return self.launch_params['launch_presentation_return_url'] + q_string

    def new_request(self):
        # TODO: Implement OutcomeRequest 
        pass
