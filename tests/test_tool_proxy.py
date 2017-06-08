import unittest
from mock import Mock, patch
from lti import ToolProxy
import requests
import json
from oauthlib.oauth1 import SignatureOnlyEndpoint

test_profile = {'@context': ['http://purl.imsglobal.org/ctx/lti/v2/ToolConsumerProfile'],
 '@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9',
 '@type': 'ToolConsumerProfile',
 'capability_offered': ['basic-lti-launch-request',
                        'User.id',
                        'Canvas.api.domain',
                        'LtiLink.custom.url',
                        'ToolProxyBinding.custom.url',
                        'ToolProxy.custom.url',
                        'Canvas.placements.accountNavigation',
                        'Canvas.placements.courseNavigation',
                        'Canvas.placements.assignmentSelection',
                        'Canvas.placements.linkSelection',
                        'Canvas.placements.postGrades',
                        'User.username',
                        'Person.email.primary',
                        'vnd.Canvas.Person.email.sis',
                        'Person.name.given',
                        'Person.name.family',
                        'Person.name.full',
                        'CourseSection.sourcedId',
                        'Person.sourcedId',
                        'Membership.role',
                        'ToolConsumerProfile.url',
                        'Security.splitSecret',
                        'Context.id',
                        'ToolConsumerInstance.guid',
                        'CourseSection.sourcedId',
                        'Membership.role',
                        'Person.email.primary',
                        'Person.name.given',
                        'Person.name.family',
                        'Person.name.full',
                        'Person.sourcedId',
                        'User.id',
                        'User.image',
                        'Message.documentTarget',
                        'Message.locale',
                        'Context.id',
                        'vnd.Canvas.root_account.uuid'],
 'guid': '339b6700-e4cb-47c5-a54f-3ee0064921a9',
 'lti_version': 'LTI-2p0',
 'product_instance': {'guid': '07adb3e60637ff02d9ea11c7c74f1ca921699bd7.canvas.instructure.com',
                      'product_info': {'product_family': {'code': 'canvas',
                                                          'vendor': {'code': 'https://instructure.com',
                                                                     'timestamp': '2008-03-27T06:00:00Z',
                                                                     'vendor_name': {'default_value': 'Instructure',
                                                                                     'key': 'vendor.name'}}},
                                       'product_name': {'default_value': 'Canvas '
                                                                         'by '
                                                                         'Instructure',
                                                        'key': 'product.name'},
                                       'product_version': 'none'},
                      'service_owner': {'description': {'default_value': 'Free '
                                                                         'For '
                                                                         'Teachers',
                                                        'key': 'service_owner.description'},
                                        'service_owner_name': {'default_value': 'Free '
                                                                                'For '
                                                                                'Teachers',
                                                               'key': 'service_owner.name'}}},
 'security_profile': [{'digest_algorithm': 'HMAC-SHA1',
                       'security_profile_name': 'lti_oauth_hash_message_security'},
                      {'digest_algorithm': 'HS256',
                       'security_profile_name': 'oauth2_access_token_ws_security'}],
 'service_offered': [{'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxy.collection',
                      '@type': 'RestService',
                      'action': ['POST'],
                      'endpoint': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_proxy',
                      'format': ['application/vnd.ims.lti.v2.toolproxy+json']},
                     {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxy.item',
                      '@type': 'RestService',
                      'action': ['GET'],
                      'endpoint': 'https://canvas.instructure.com/api/lti/tool_proxy/{tool_proxy_guid}',
                      'format': ['application/vnd.ims.lti.v2.toolproxy+json']},
                     {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#vnd.Canvas.authorization',
                      '@type': 'RestService',
                      'action': ['POST'],
                      'endpoint': 'https://canvas.instructure.com/api/lti/courses/1157004/authorize',
                      'format': ['application/json']},
                     {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxySettings',
                      '@type': 'RestService',
                      'action': ['GET', 'PUT'],
                      'endpoint': 'https://canvas.instructure.com/api/lti/tool_settings/tool_proxy/{tool_proxy_id}',
                      'format': ['application/vnd.ims.lti.v2.toolsettings+json',
                                 'application/vnd.ims.lti.v2.toolsettings.simple+json']},
                     {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxyBindingSettings',
                      '@type': 'RestService',
                      'action': ['GET', 'PUT'],
                      'endpoint': 'https://canvas.instructure.com/api/lti/tool_settings/bindings/{binding_id}',
                      'format': ["application/vnd.ims.lti.v2.toolsettings+json'",
                                 'application/vnd.ims.lti.v2.toolsettings.simple+json']},
                     {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#LtiLinkSettings',
                      '@type': 'RestService',
                      'action': ['GET', 'PUT'],
                      'endpoint': 'https://canvas.instructure.com/api/lti/tool_settings/links/{tool_proxy_id}',
                      'format': ['application/vnd.ims.lti.v2.toolsettings+json',
                                 'application/vnd.ims.lti.v2.toolsettings.simple+json']}]}

test_params = {'ext_api_domain': 'canvas.instructure.com',
 'ext_tool_consumer_instance_guid': '07adb3e60637ff02d9ea11c7c74f1ca921699bd7.canvas.instructure.com',
 'launch_presentation_document_target': 'iframe',
 'launch_presentation_return_url': 'https://canvas.instructure.com/courses/1157004/lti/registration_return',
 'lti_message_type': 'ToolProxyRegistrationRequest',
 'lti_version': 'LTI-2p0',
 'reg_key': 'eb9031ac-2e12-422e-8238-beb9c41419b3',
 'reg_password': 'f781d41d-6f9e-4b02-b11b-fe4ffa704ac1',
 'tc_profile_url': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile'}


class TestToolProxy(unittest.TestCase):
    def test_load_tc_profile(self):
        #Mock out the call to the requests library
        response = Mock()
        response.text = json.dumps(test_profile)

        proxy = ToolProxy(params=test_params)

        with patch('lti.tool_proxy.requests.get') as mock_get:
            mock_get.return_value = response
            proxy.load_tc_profile()

        self.assertEqual(proxy.tc_profile, test_profile)

    def test_tool_consumer_profile_url(self):
        proxy = ToolProxy(params=test_params)

        self.assertEqual(proxy.tool_consumer_profile_url, test_params['tc_profile_url'])

    def test_find_registration_url(self):
        proxy = ToolProxy(params=test_params)
        proxy.tc_profile = test_profile

        registration_url = proxy.find_registration_url()

        self.assertEqual(registration_url, 'https://canvas.instructure.com/api/lti/courses/1157004/tool_proxy')

    def test_not_find_registration_url(self):
        proxy = ToolProxy(params=test_params)
        proxy.tc_profile = {'@context': ['http://purl.imsglobal.org/ctx/lti/v2/ToolConsumerProfile'],
                             '@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9',
                             '@type': 'ToolConsumerProfile',
                             'capability_offered': ['basic-lti-launch-request',
                                                    'vnd.Canvas.root_account.uuid'],
                             'guid': '339b6700-e4cb-47c5-a54f-3ee0064921a9',
                             'lti_version': 'LTI-2p0',
                             'product_instance': {'guid': '07adb3e60637ff02d9ea11c7c74f1ca921699bd7.canvas.instructure.com',
                                                  'product_info': {'product_family': {'code': 'canvas',
                                                                                      'vendor': {'code': 'https://instructure.com',
                                                                                                 'timestamp': '2008-03-27T06:00:00Z',
                                                                                                 'vendor_name': {'default_value': 'Instructure',
                                                                                                                 'key': 'vendor.name'}}},
                                                                   'product_name': {'default_value': 'Canvas '
                                                                                                     'by '
                                                                                                     'Instructure',
                                                                                    'key': 'product.name'},
                                                                   'product_version': 'none'},
                                                  'service_owner': {'description': {'default_value': 'Free '
                                                                                                     'For '
                                                                                                     'Teachers',
                                                                                    'key': 'service_owner.description'},
                                                                    'service_owner_name': {'default_value': 'Free '
                                                                                                            'For '
                                                                                                            'Teachers',
                                                                                           'key': 'service_owner.name'}}},
                             'security_profile': [{'digest_algorithm': 'HMAC-SHA1',
                                                   'security_profile_name': 'lti_oauth_hash_message_security'},
                                                  {'digest_algorithm': 'HS256',
                                                   'security_profile_name': 'oauth2_access_token_ws_security'}],
                             'service_offered': [{'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxy.item',
                                                  '@type': 'RestService',
                                                  'action': ['GET'],
                                                  'endpoint': 'https://canvas.instructure.com/api/lti/tool_proxy/{tool_proxy_guid}',
                                                  'format': ['application/vnd.ims.lti.v2.toolproxy+json']},
                                                 {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#vnd.Canvas.authorization',
                                                  '@type': 'RestService',
                                                  'action': ['POST'],
                                                  'endpoint': 'https://canvas.instructure.com/api/lti/courses/1157004/authorize',
                                                  'format': ['application/json']},
                                                 {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxySettings',
                                                  '@type': 'RestService',
                                                  'action': ['GET', 'PUT'],
                                                  'endpoint': 'https://canvas.instructure.com/api/lti/tool_settings/tool_proxy/{tool_proxy_id}',
                                                  'format': ['application/vnd.ims.lti.v2.toolsettings+json',
                                                             'application/vnd.ims.lti.v2.toolsettings.simple+json']},
                                                 {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#ToolProxyBindingSettings',
                                                  '@type': 'RestService',
                                                  'action': ['GET', 'PUT'],
                                                  'endpoint': 'https://canvas.instructure.com/api/lti/tool_settings/bindings/{binding_id}',
                                                  'format': ["application/vnd.ims.lti.v2.toolsettings+json'",
                                                             'application/vnd.ims.lti.v2.toolsettings.simple+json']},
                                                 {'@id': 'https://canvas.instructure.com/api/lti/courses/1157004/tool_consumer_profile/339b6700-e4cb-47c5-a54f-3ee0064921a9#LtiLinkSettings',
                                                  '@type': 'RestService',
                                                  'action': ['GET', 'PUT'],
                                                  'endpoint': 'https://canvas.instructure.com/api/lti/tool_settings/links/{tool_proxy_id}',
                                                  'format': ['application/vnd.ims.lti.v2.toolsettings+json',
                                                             'application/vnd.ims.lti.v2.toolsettings.simple+json']}]}

        registration_url = proxy.find_registration_url()

        self.assertIsNone(registration_url)

    def test_register_proxy(self):
        proxy = ToolProxy(params=test_params)
        proxy.tc_profile = test_profile

        signed_request = proxy.register_proxy({'tool_profile': 'A Real Tool Profile Goes here'})

        self.assertIsInstance(signed_request, requests.PreparedRequest)