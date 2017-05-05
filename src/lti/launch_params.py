import sys
from collections import MutableMapping

from . import DEFAULT_LTI_VERSION

py = sys.version_info
if py < (2, 6, 0):
    bytes = str


def touni(s, enc='utf8', err='strict'):
    return s.decode(enc, err) if isinstance(s, bytes) else unicode(s)


LAUNCH_PARAMS_REQUIRED = [
    'lti_message_type',
    'lti_version',
    'resource_link_id'
]

LAUNCH_PARAMS_RECOMMENDED = [
    'resource_link_description',
    'resource_link_title',
    'user_id',
    'user_image',
    'roles',
    'lis_person_name_given',
    'lis_person_name_family',
    'lis_person_name_full',
    'lis_person_contact_email_primary',
    'role_scope_mentor',
    'context_id',
    'context_label',
    'context_title',
    'context_type',
    'launch_presentation_locale',
    'launch_presentation_document_target',
    'launch_presentation_css_url',
    'launch_presentation_width',
    'launch_presentation_height',
    'launch_presentation_return_url',
    'tool_consumer_info_product_family_code',
    'tool_consumer_info_version',
    'tool_consumer_instance_guid',
    'tool_consumer_instance_name',
    'tool_consumer_instance_description',
    'tool_consumer_instance_url',
    'tool_consumer_instance_contact_email',
]

LAUNCH_PARAMS_LIS = [
    'lis_course_section_sourcedid',
    'lis_course_offering_sourcedid',
    'lis_outcome_service_url',
    'lis_person_sourcedid',
    'lis_result_sourcedid',
]

LAUNCH_PARAMS_RETURN_URL = [
    'lti_errormsg',
    'lti_errorlog',
    'lti_msg',
    'lti_log'
]

LAUNCH_PARAMS_OAUTH = [
    'oauth_consumer_key',
    'oauth_signature_method',
    'oauth_timestamp',
    'oauth_nonce',
    'oauth_version',
    'oauth_signature',
    'oauth_callback'
]

LAUNCH_PARAMS_IS_LIST = [
    'roles',
    'role_scope_mentor',
    'context_type',
    'accept_media_types',
    'accept_presentation_document_targets'
]

LAUNCH_PARAMS_CANVAS = [
    'selection_directive',
    'text'
]

CONTENT_PARAMS_REQUEST = [
    'accept_media_types',
    'accept_presentation_document_targets',
    'content_item_return_url',
    'accept_unsigned',
    'accept_multiple',
    'accept_copy_advice',
    'auto_create',
    'title',
    'data',
    'can_confirm'
]

CONTENT_PARAMS_RESPONSE = [
    'content_items',
    'lti_msg',
    'lti_log',
    'lti_errormsg',
    'lti_errorlog'
]

CONTENT_PARAMS_REQUIRED = [
    'lti_message_type',
    'lti_version'
]

REGISTRATION_PARAMS = [
    'tc_profile_url',
    'reg_password',
    'reg_key'
]

LAUNCH_PARAMS = (
    LAUNCH_PARAMS_REQUIRED +
    LAUNCH_PARAMS_RECOMMENDED +
    LAUNCH_PARAMS_RETURN_URL +
    LAUNCH_PARAMS_OAUTH +
    LAUNCH_PARAMS_LIS +
    LAUNCH_PARAMS_CANVAS +
    CONTENT_PARAMS_REQUEST +
    CONTENT_PARAMS_RESPONSE +
    REGISTRATION_PARAMS
)


def valid_param(param):
    if param.startswith('custom_') or param.startswith('ext_'):
        return True
    elif param in LAUNCH_PARAMS:
        return True
    return False


class InvalidLaunchParamError(ValueError):

    def __init__(self, param):
        message = "{} is not a valid launch param".format(param)
        super(Exception, self).__init__(message)


class LaunchParams(MutableMapping):
    """
    Represents the params for an LTI launch request. Provides dict-like
    behavior through the use of the MutableMapping ABC mixin.  Strictly
    enforces that params are valid LTI params.
    """

    def __init__(self, *args, **kwargs):

        self._params = dict()
        self.update(*args, **kwargs)

        # now verify we only got valid launch params
        for k in self.keys():
            if not valid_param(k):
                raise InvalidLaunchParamError(k)

        # enforce some defaults
        if 'lti_version' not in self:
            self['lti_version'] = DEFAULT_LTI_VERSION
        if 'lti_message_type' not in self:
            self['lti_message_type'] = 'basic-lti-launch-request'

    def set_non_spec_param(self, param, val):
        self._params[param] = val

    def get_non_spec_param(self, param):
        return self._params.get(param)

    def _param_value(self, param):
        if param in LAUNCH_PARAMS_IS_LIST:
            return [x.strip() for x in self._params[param].split(',')]
        else:
            return self._params[param]

    def __len__(self):
        return len(self._params)

    def __getitem__(self, item):
        if not valid_param(item):
            raise KeyError("{} is not a valid launch param".format(item))
        try:
            return self._param_value(item)
        except KeyError:
            # catch and raise new KeyError in the proper context
            raise KeyError(item)

    def __setitem__(self, key, value):
        if not valid_param(key):
            raise InvalidLaunchParamError(key)
        if key in LAUNCH_PARAMS_IS_LIST:
            if isinstance(value, list):
                value = ','.join([x.strip() for x in value])
        self._params[key] = value

    def __delitem__(self, key):
        if key in self._params:
            del self._params[key]

    def __iter__(self):
        return iter(self._params)
