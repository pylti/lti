from collections import defaultdict

# List of the standard launch parameters for an LTI launch
LAUNCH_DATA_PARAMETERS = [
    'context_id',
    'context_label',
    'context_title',
    'context_type',
    'launch_presentation_css_url',
    'launch_presentation_document_target',
    'launch_presentation_height',
    'launch_presentation_locale',
    'launch_presentation_return_url',
    'launch_presentation_width',
    'lis_course_section_sourcedid',
    'lis_outcome_service_url',
    'lis_person_contact_email_primary',
    'lis_person_name_family',
    'lis_person_name_full',
    'lis_person_name_given',
    'lis_person_sourcedid',
    'lis_result_sourcedid',
    'lti_message_type',
    'lti_version',
    'oauth_callback',
    'oauth_consumer_key',
    'oauth_nonce',
    'oauth_signature',
    'oauth_signature_method',
    'oauth_timestamp',
    'oauth_version',
    'resource_link_description',
    'resource_link_id',
    'resource_link_title',
    'roles',
    'tool_consumer_info_product_family_code',
    'tool_consumer_info_version',
    'tool_consumer_instance_contact_email',
    'tool_consumer_instance_description',
    'tool_consumer_instance_guid',
    'tool_consumer_instance_name',
    'tool_consumer_instance_url',
    'user_id',
    'user_image'
]


class LaunchParamsMixin(object):
    def __init__(self):
        super(LaunchParamsMixin, self).__init__()

        for param in LAUNCH_DATA_PARAMETERS:
            setattr(self, param, None)

        # We only support oauth 1.0 for now
        self.oauth_version = '1.0'

        # These dictionaries return a 'None' object when accessing a key that
        # is not in the dictionary.
        self.custom_params = defaultdict(lambda: None)
        self.ext_params = defaultdict(lambda: None)

    def roles(self, roles_list):
        '''
        Set the roles for the current launch.

        Full list of roles can be found here:
        http://www.imsglobal.org/LTI/v1p1pd/ltiIMGv1p1pd.html#_Toc309649700

        LIS roles include:
        * Student
        * Faculty
        * Member
        * Learner
        * Instructor
        * Mentor
        * Staff
        * Alumni
        * ProspectiveStudent
        * Guest
        * Other
        * Administrator
        * Observer
        * None
        '''
        if roles_list and isinstance(roles_list, list):
            self.roles = [].extend(roles_list)
        elif roles_list and isinstance(roles_list, basestring):
            self.roles = [role.lower() for role in roles_list.split(',')]

    def process_params(self, params):
        '''
        Populates the launch data from a dictionary. Only cares about keys in
        the LAUNCH_DATA_PARAMETERS list, or that start with 'custom_' or
        'ext_'.
        '''
        for key, val in params.items():
            if key in LAUNCH_DATA_PARAMETERS and val != 'None':
                if key == 'roles':
                    if isinstance(val, list):
                        # If it's already a list, no need to parse
                        self.roles = list(val)
                    else:
                        # If it's a ',' delimited string, split
                        self.roles = val.split(',')
                else:
                    setattr(self, key, unicode(val))
            elif 'custom_' in key:
                self.custom_params[key] = unicode(val)
            elif 'ext_' in key:
                self.ext_params[key] = unicode(val)

    def set_custom_param(self, key, val):
        self.custom_params['custom_' + key] = val

    def get_custom_param(self, key):
        return self.custom_params['custom_' + key]

    def set_non_spec_param(self, key, val):
        self.non_spec_params[key] = val

    def get_non_spec_param(self, key):
        return self.non_spec_params[key]

    def set_ext_param(self, key, val):
        self.ext_params['ext_' + key] = val

    def get_ext_param(self, key):
        return self.ext_params['ext_' + key]

    def to_params(self):
        '''
        Createa a new dictionary with all launch data. Custom / Extension keys
        will be included. Roles are set as a ',' separated string.
        '''
        params = {}
        custom_params = {}
        for key in self.custom_params:
            custom_params[key] = self.custom_params[key]
        ext_params = {}
        for key in self.ext_params:
            ext_params[key] = self.ext_params[key]
        for key in LAUNCH_DATA_PARAMETERS:
            if hasattr(self, key):
                params[key] = getattr(self, key)
        params.update(custom_params)
        params.update(ext_params)
        return params
