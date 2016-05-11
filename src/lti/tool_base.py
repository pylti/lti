
from launch_params import LaunchParams, valid_param

ROLES_STUDENT = ['student', 'learner']
ROLES_INSTRUCTOR = ['instructor', 'faculty', 'staff']

class ToolBase(object):

    def __init__(self, consumer_key, consumer_secret, params=None):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        if params is None:
            params = {}

        if isinstance(params, LaunchParams):
            self.launch_params = params
        else:
            self.launch_params = LaunchParams(params)

    def __getattr__(self, attr):
        if not valid_param(attr):
            raise AttributeError(
                "{} is not a valid launch param attribute".format(attr))
        try:
            return self.launch_params[attr]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        if valid_param(key):
            self.launch_params[key] = value
        else:
            self.__dict__[key] = value

    def has_role(self, role):
        return self.launch_params.get('roles') and any(
               x.lower() == role.lower() for x in self.launch_params['roles'])

    def is_student(self):
        return any(self.has_role(x) for x in ROLES_STUDENT)

    def is_instructor(self):
        return any(self.has_role(x) for x in ROLES_INSTRUCTOR)

    def is_launch_request(self):
        msg_type = self.launch_params.get('lti_message_type')
        return msg_type == 'basic-lti-launch-request'

    def set_custom_param(self, key, val):
        setattr(self, 'custom_' + key, val)

    def get_custom_param(self, key):
        return getattr(self, 'custom_' + key)

    def set_non_spec_param(self, key, val):
        self.launch_params.set_non_spec_param(key, val)

    def get_non_spec_param(self, key):
        return self.launch_params.get_non_spec_param(key)

    def set_ext_param(self, key, val):
        setattr(self, 'ext_' + key, val)

    def get_ext_param(self, key):
        return getattr(self, 'ext_' + key)

    def to_params(self):
        params = dict(self.launch_params)
        # stringify any list values
        for k,v in params.iteritems():
            if isinstance(v, list):
                params[k] = ','.join(v)
        return params
