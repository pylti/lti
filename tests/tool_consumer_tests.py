from test_helper import create_test_tc
from tool_consumer import ToolConsumer

import unittest

class TestToolConsumer(unittest.TestCase):
    def setUp(self):
        self.tc = ToolConsumer.new('12345', 'secret')
    @tc.launch_url = 'http://dr-chuck.com/ims/php-simple/tool.php'
    @tc.timestamp = '1251600739'
    @tc.nonce = 'c8350c0e47782d16d2fa48b2090c1d8f'

    @tc.resource_link_id = '120988f929-274612'
    @tc.user_id = '292832126'
    @tc.roles = 'Instructor'
    @tc.lis_person_name_full = 'Jane Q. Public'
    @tc.lis_person_contact_email_primary = 'user@school.edu'
    @tc.set_non_spec_param('lis_person_sourced_id', 'school.edu:user')
    @tc.context_id = '456434513'
    @tc.context_title = 'Design of Personal Environments'
    @tc.context_label = 'SI182'
    @tc.lti_version = 'LTI-1p0'
    @tc.lti_message_type = 'basic-lti-launch-request'
    @tc.tool_consumer_instance_guid = 'lmsng.school.edu'
    @tc.tool_consumer_instance_description = 'University of School (LMSng)'
    @tc.set_non_spec_param('basiclti_submit', 'Launch Endpoint with BasicLTI Data')
