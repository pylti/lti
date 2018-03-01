import unittest

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit  # Python 2

from mock import Mock, patch
from oauthlib.common import generate_client_id
from oauthlib.common import generate_token
from oauthlib.oauth1 import SignatureOnlyEndpoint
from oauthlib.oauth1 import RequestValidator

from lti import LaunchParams, OutcomeRequest, ToolProvider
from lti.utils import parse_qs, InvalidLTIConfigError
from lti.tool_provider import ProxyValidator

def create_tp(key=None, secret=None, lp=None, launch_url=None,
              launch_headers=None, tp_class=ToolProvider):
    key = key or generate_client_id()
    secret = secret or generate_token()
    launch_params = tp_class.launch_params_class()
    if lp is not None:
        launch_params.update(lp)
    launch_url = launch_url or "http://example.edu"
    launch_headers = launch_headers or {}
    return tp_class(key, secret, launch_params, launch_url, launch_headers)

class CustomLaunchParams(LaunchParams):
    def valid_param(self, param):
        result  = super(CustomLaunchParams, self).valid_param(param)
        if not result:
            if param in ['basiclti_submit', 'launch_url']:
                result = True

        return result

class CustomToolProvider(ToolProvider):
    launch_params_class = CustomLaunchParams

class TestToolProvider(unittest.TestCase):

    def test_constructor(self):
        tp = create_tp()
        self.assertIsInstance(tp.launch_params, LaunchParams)

        tp = create_tp(launch_headers={'foo': 'bar'})
        self.assertEqual(tp.launch_headers['foo'], 'bar')

    def test_is_valid_request(self):
        """
        just checks that the TP sends the correct args to the endpoint
        """
        key = generate_client_id()
        secret = generate_token()
        lp = {
            'lti_version': 'foo',
            'lti_message_type': 'bar',
            'resource_link_id': 123
        }
        launch_url = 'http://example.edu/foo/bar'
        launch_headers = {'Content-Type': 'baz'}
        tp = create_tp(key, secret, lp, launch_url, launch_headers)

        with patch.object(SignatureOnlyEndpoint, 'validate_request') as mv:
            mv.return_value = True, None  # Tuple of valid, request
            self.assertTrue(tp.is_valid_request(Mock()))
            call_url, call_method, call_params, call_headers = mv.call_args[0]
            self.assertEqual(call_url, launch_url)
            self.assertEqual(call_method, 'POST')
            self.assertEqual(call_params, lp)
            self.assertEqual(call_headers, launch_headers)

    def test_is_valid_request_no_key_or_secret(self):
        """
        Checks that the key and secret will be populated during validation.
        """
        key = 'spamspamspam'
        secret_ = 'eggseggsegss'
        lp = LaunchParams({
            'lti_version': 'foo',
            'lti_message_type': 'bar',
            'resource_link_id': '123',
            'oauth_consumer_key': key,
            'oauth_nonce': '9069031379649850801466828504',
            'oauth_timestamp': '1466828504',
            'oauth_version': '1.0',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_signature': 'WZ9IHyFnKgDKBvnAfNSL3aOVteg=',
        })
        launch_url = 'https://example.edu/foo/bar'
        launch_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        class TpValidator(RequestValidator):
            dummy_client = ''
            def validate_timestamp_and_nonce(self, timestamp, nonce, request,
                                             request_token=None,
                                             access_token=None):
                return True
            def validate_client_key(self, client_key, request):
                return True
            def get_client_secret(self, client_key, request):
                return secret_
            secret = secret_  # Fool the ProxyValidator

        tp = ToolProvider(params=lp, launch_url=launch_url,
                          launch_headers=launch_headers)

        SOE = SignatureOnlyEndpoint
        with patch.object(SOE, '_check_mandatory_parameters'):
            with patch.object(SOE, '_check_signature', return_value=True):
                self.assertTrue(tp.is_valid_request(TpValidator()))

        self.assertEqual(tp.consumer_key, key)
        self.assertEqual(tp.consumer_secret, secret_)

    def test_proxy_validator(self):
        '''
        Should store the secret when get_client_secret is called.
        '''
        class TpValidator(RequestValidator):
            def get_client_secret(self, client_key, request):
                return 'eggseggseggs'

        pv = ProxyValidator(TpValidator())
        self.assertFalse(hasattr(pv, 'secret'))
        self.assertEqual(
            pv.get_client_secret('spamspamspam', None), 'eggseggseggs')
        self.assertEqual(pv.secret, 'eggseggseggs')

    def test_outcome_service(self):
        '''
        Should recognize an outcome service.
        '''
        tp = create_tp()
        self.assertFalse(tp.is_outcome_service())
        tp = create_tp(lp={'lis_result_sourcedid': 1})
        self.assertFalse(tp.is_outcome_service())
        tp = create_tp(lp={
            'lis_outcome_service_url': 'foo',
            'lis_result_sourcedid': 1
        })
        self.assertTrue(tp.is_outcome_service())

    def test_return_url_with_messages(self):
        '''
        Should generate a return url with messages.
        '''
        tp = create_tp()
        self.assertIsNone(tp.build_return_url())

        tp = create_tp(lp={
            'launch_presentation_return_url': 'http://foo.edu/done'
        })
        self.assertEqual(tp.build_return_url(), 'http://foo.edu/done')

        tp = create_tp(lp={
            'launch_presentation_return_url': 'http://foo.edu/done',
            'lti_errormsg': 'user error',
            'lti_errorlog': 'lms error',
            'lti_msg': 'user message',
            'lti_log': 'lms message'
        })
        return_url = tp.build_return_url()
        parsed = urlsplit(return_url)
        self.assertEqual(parsed.hostname, 'foo.edu')
        self.assertEqual(parsed.path, '/done')
        self.assertEqual(parse_qs(parsed.query), {
            'lti_errormsg': 'user error',
            'lti_errorlog': 'lms error',
            'lti_msg': 'user message',
            'lti_log': 'lms message'
        })

    def test_username(self):
        '''
        Should find the best username.
        '''
        tp = create_tp()
        self.assertEqual(tp.username('guy'), 'guy')
        tp.lis_person_name_full = 'full'
        self.assertEqual(tp.username('guy'), 'full')
        tp.lis_person_name_family = 'family'
        self.assertEqual(tp.username('guy'), 'family')
        tp.lis_person_name_given = 'given'
        self.assertEqual(tp.username('guy'), 'given')

    def test_new_request(self):
        key = generate_client_id()
        secret = generate_token()
        lp = {
            'lti_version': 'foo',
            'lti_message_type': 'bar',
            'resource_link_id': 123
        }
        tp = create_tp(key, secret, lp)
        req = tp.new_request({})
        self.assertIsInstance(req, OutcomeRequest)
        self.assertEqual(req, tp._last_outcome_request)
        self.assertEqual(req.consumer_key, key)
        self.assertEqual(len(tp.outcome_requests), 1)

        # outcome request should get assigned attr
        req = tp.new_request({'score': 1.0})
        self.assertEqual(req.score, 1.0)
        self.assertEqual(len(tp.outcome_requests), 2)

        # but can't override some fields
        req = tp.new_request({'consumer_key': 'foo'})
        self.assertEqual(req.consumer_key, key)
        self.assertEqual(len(tp.outcome_requests), 3)

        # should fail if we use an invalid opt
        self.assertRaises(InvalidLTIConfigError, tp.new_request, {'foo': 1})
        self.assertEqual(len(tp.outcome_requests), 3)


    def test_last_outcome_success(self):
        tp = create_tp()
        mock = Mock()
        mock.was_outcome_post_successful.return_value = True
        tp._last_outcome_request = mock
        self.assertTrue(tp.last_outcome_success())

    def test_last_outcome_request(self):
        tp = create_tp()
        tp.outcome_requests = ['foo','bar']
        self.assertEqual(tp.last_outcome_request(), 'bar')

    def test_custom_launch_params(self):
        key = generate_client_id()
        secret = generate_token()
        lp = {
            'lti_version': 'foo',
            'lti_message_type': 'bar',
            'resource_link_id': 123,
            'launch_url': 'more_foo',
            'basiclti_submit': 'more_bar'
        }
        launch_url = 'http://example.edu/foo/bar'
        launch_headers = {'Content-Type': 'baz'}
        tp = create_tp(key, secret, lp, launch_url, launch_headers, tp_class=CustomToolProvider)

        with patch.object(SignatureOnlyEndpoint, 'validate_request') as mv:
            mv.return_value = True, None  # Tuple of valid, request
            self.assertTrue(tp.is_valid_request(Mock()))
            call_url, call_method, call_params, call_headers = mv.call_args[0]
            self.assertEqual(call_url, launch_url)
            self.assertEqual(call_method, 'POST')
            self.assertEqual(call_params, lp)
            self.assertEqual(call_headers, launch_headers)

# mock the django.shortcuts import to allow testing
mock = Mock()
mock.shortcuts.redirect.return_value = 'foo'
mock_modules = {
    'django': mock,
    'django.shortcuts': mock.shortcuts
}

class TestDjangoToolProvider(unittest.TestCase):

    @patch.dict('sys.modules', mock_modules)
    def test_from_django_request(self):
        from lti.contrib.django import DjangoToolProvider
        secret = generate_token()
        mock_req = Mock()
        mock_req.POST = {'oauth_consumer_key': 'foo'}
        mock_req.META = {'CONTENT_TYPE': 'bar'}
        mock_req.build_absolute_uri.return_value = 'http://example.edu/foo/bar'
        tp = DjangoToolProvider.from_django_request(secret, mock_req)
        self.assertEqual(tp.consumer_key, 'foo')
        self.assertEqual(tp.launch_headers['CONTENT_TYPE'], 'bar')
        self.assertEqual(tp.launch_url, 'http://example.edu/foo/bar')

    @patch.dict('sys.modules', mock_modules)
    def test_request_required(self):
        from lti.contrib.django import DjangoToolProvider
        with self.assertRaises(ValueError):
            DjangoToolProvider.from_django_request()

    @patch.dict('sys.modules', mock_modules)
    def test_secret_not_required(self):
        from lti.contrib.django import DjangoToolProvider
        mock_req = Mock()
        mock_req.POST = {'oauth_consumer_key': 'foo'}
        mock_req.META = {'CONTENT_TYPE': 'bar'}
        mock_req.build_absolute_uri.return_value = 'http://example.edu/foo/bar'
        tp = DjangoToolProvider.from_django_request(request=mock_req)
        self.assertEqual(tp.consumer_key, 'foo')
        self.assertEqual(tp.launch_headers['CONTENT_TYPE'], 'bar')
        self.assertEqual(tp.launch_url, 'http://example.edu/foo/bar')

    @patch.dict('sys.modules', mock_modules)
    def test_success_redirect(self):
        from lti.contrib.django import DjangoToolProvider
        tp = create_tp(lp={
            'launch_presentation_return_url': 'http://example.edu/foo'
        }, tp_class=DjangoToolProvider)
        redirect_retval = tp.success_redirect(msg='bar', log='baz')
        self.assertEqual(redirect_retval, 'foo')
        redirect_url, = mock.shortcuts.redirect.call_args[0]
        parsed = urlsplit(redirect_url)
        self.assertEqual(parse_qs(parsed.query), {
            'lti_msg': 'bar',
            'lti_log': 'baz'
        })

    @patch.dict('sys.modules', mock_modules)
    def test_error_redirect(self):
        from lti.contrib.django import DjangoToolProvider
        tp = create_tp(lp={
            'launch_presentation_return_url': 'http://example.edu/bar'
        }, tp_class=DjangoToolProvider)
        redirect_retval = tp.error_redirect(errormsg='abcd', errorlog='efgh')
        self.assertEqual(redirect_retval, 'foo')
        redirect_url, = mock.shortcuts.redirect.call_args[0]
        parsed = urlsplit(redirect_url)
        self.assertEqual(parse_qs(parsed.query), {
            'lti_errormsg': 'abcd',
            'lti_errorlog': 'efgh'
        })

class TestFlaskToolProvider(unittest.TestCase):

    def test_from_flask_request(self):
        from lti.contrib.flask import FlaskToolProvider
        secret = generate_token()
        mock_req = Mock()
        mock_req.form = {'oauth_consumer_key': 'foo'}
        mock_req.headers = {'Content-type': 'bar'}
        mock_req.url = 'http://example.edu/foo/bar'
        tp = FlaskToolProvider.from_flask_request(secret, mock_req)
        self.assertEqual(tp.consumer_key, 'foo')
        self.assertEqual(tp.launch_headers['Content-type'], 'bar')
        self.assertEqual(tp.launch_url, 'http://example.edu/foo/bar')

    def test_request_required(self):
        from lti.contrib.flask import FlaskToolProvider
        with self.assertRaises(ValueError):
            FlaskToolProvider.from_flask_request()

    def test_secret_not_required(self):
        from lti.contrib.flask import FlaskToolProvider
        mock_req = Mock()
        mock_req.form = {'oauth_consumer_key': 'foo'}
        mock_req.headers = {'Content-type': 'bar'}
        mock_req.url = 'http://example.edu/foo/bar'
        tp = FlaskToolProvider.from_flask_request(request=mock_req)
        self.assertEqual(tp.consumer_key, 'foo')
        self.assertEqual(tp.launch_headers['Content-type'], 'bar')
        self.assertEqual(tp.launch_url, 'http://example.edu/foo/bar')
