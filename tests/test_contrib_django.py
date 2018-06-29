from django.test import TestCase, RequestFactory, override_settings
from django.conf import settings
from django.urls import reverse
from django.contrib import auth
from django.core.exceptions import PermissionDenied

import hashlib
import time

import lti

from . import utils, backends

UserModel = auth.get_user_model()

consumer_key = u'TESTKEYdyicekaj3utnolOlop'
consumer_secret = u'TESTSECRETyunRokMydFreidCeb7'

lti_consumer_secrets = {
    consumer_key: consumer_secret
}


def _get_default_params():
    return {
        'lti_message_type': 'basic-lti-launch-request',
        'lti_version': 'LTI-1p0',
        'resource_link_id': '123',
    }


def _generate_username_from_valid_params(consumer_key, user_id):
        return '_%s_%s' % (consumer_key, user_id)


@override_settings(LTI_CONSUMER_SECRETS=lti_consumer_secrets)
class LtiConsumerSettingsStorageTests(TestCase):

    def setUp(self):
        self.store = utils.LtiConsumerSettingsStorage()

    # Decorated separately because we need to del the LTI_CONSUMER_SECRETS
    # setting for this method only.
    @override_settings()
    def test_set_secrets_to_empty_when_no_settings(self):
        del settings.LTI_CONSUMER_SECRETS

        store = utils.LtiConsumerSettingsStorage()
        self.assertIsNone(store.get_consumer_secret(consumer_key))

    def test_get_consumer_secret_key_existing(self):
        self.assertEqual(consumer_secret,
                         self.store.get_consumer_secret(consumer_key))

    def test_get_consumer_secret_key_missing(self):
        self.assertIsNone(self.store.get_consumer_secret('missingkey'))


class LtiConsumerFakeStorage(object):
    pass


class LtiConsumerStorageSettingTests(TestCase):
    # Decorated with an empty override because we need to del the
    # LTI_CONSUMER_STORAGE setting.
    @override_settings()
    def test_setting_missing(self):
        del settings.LTI_CONSUMER_STORAGE

        self.assertIsInstance(utils.get_lti_consumer_storage(),
                              utils.LtiConsumerSettingsStorage)

    def test_setting_correct(self):
        engine_string = __name__+'.LtiConsumerFakeStorage'
        with self.settings(LTI_CONSUMER_STORAGE=engine_string):
            self.assertIsInstance(utils.get_lti_consumer_storage(),
                                  LtiConsumerFakeStorage)

    def test_setting_bad_module(self):
        engine_string = __name__+'.MissingFakeStore'
        with self.settings(LTI_CONSUMER_STORAGE=engine_string):
            with self.assertRaises(ImportError):
                utils.get_lti_consumer_storage()


@override_settings(
    LTI_CONSUMER_SECRETS=lti_consumer_secrets,
    LTI_ENFORCE_SSL=False,
)
class LtiBackendTests(TestCase):
    @staticmethod
    def _get_requests_from_params(params):
        r = RequestFactory().get('/')
        launch_url = r.build_absolute_uri('/')

        tool_consumer = lti.ToolConsumer(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            launch_url=launch_url,
            params=params,
        )

        launch_data = tool_consumer.generate_launch_data()

        # This is a workaround to what seems to be a discrepency between how
        # the ToolProvider and ToolConsumer encode the oauth_signature field.
        launch_data['oauth_signature'] = (
            launch_data['oauth_signature'].replace(' ', '+'))

        django_request = RequestFactory().post(
            '/',
            launch_data,
        )

        launch_request = (
            lti.contrib.django.DjangoToolProvider.from_django_request(
                    request=django_request,
                )
            )

        return django_request, launch_request

    def _authenticate_with_params(self, params, backend=None):
        if not backend:
            backend = self._get_backend()

        django_request, launch_request = (
            self._get_requests_from_params(params))

        user_count_before = UserModel.objects.count()
        user = backend.authenticate(django_request, launch_request)
        user_count_after = UserModel.objects.count()

        user_created = (user_count_after - 1 == user_count_before)

        return user, user_created

    def _get_backend(self):
        return backends.LtiBackend()

    def test__generate_username_with_valid_params(self):
        params = _get_default_params()
        params['user_id'] = 'testing-user_id-valid'

        django_request, launch_request = (
            self._get_requests_from_params(params))

        self.assertEqual(
            '_%s_%s' % (consumer_key, params['user_id']),
            self._get_backend()._generate_username(launch_request),
        )

    def test__generate_username_with_invalid_params(self):
        params = _get_default_params()
        params['user_id'] = 'testing-user_id-invalid-%*'

        django_request, launch_request = self._get_requests_from_params(params)

        self.assertNotEqual(
            '_%s_%s' % (consumer_key, params['user_id']),
            self._get_backend()._generate_username(launch_request),
        )
        self.assertEqual(
            '_%s_%s' % (
                consumer_key,
                hashlib.sha1(params['user_id'].encode()).hexdigest()
            ),
            self._get_backend()._generate_username(launch_request),
        )

    def test_authenicate_with_invalid_signature(self):
        params = _get_default_params()
        params['user_id'] = 'test-user-with-invalid-signature'

        django_request, launch_request = (
            self._get_requests_from_params(params))

        launch_request.oauth_signature = 'wrong'

        user_count_before = UserModel.objects.count()
        with self.assertRaises(PermissionDenied):
            self._get_backend().authenticate(django_request, launch_request)
        user_count_after = UserModel.objects.count()

        user_created = (user_count_after - 1 == user_count_before)

        self.assertFalse(user_created)

    def test_authenicate_with_tampered_content(self):
        params = _get_default_params()
        params['user_id'] = 'test-user-with-tampered-content'

        django_request, launch_request = (
            self._get_requests_from_params(params))

        launch_request.user_id = 'anotherUsersId'

        user_count_before = UserModel.objects.count()
        with self.assertRaises(PermissionDenied):
            self._get_backend().authenticate(django_request, launch_request)
        user_count_after = UserModel.objects.count()

        user_created = (user_count_after - 1 == user_count_before)

        self.assertFalse(user_created)

    def test_authenicate_without_user_id(self):
        params = _get_default_params()

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user.is_anonymous)
        self.assertFalse(user_created)

    def test_authenicate_with_user_id(self):
        params = _get_default_params()
        params['user_id'] = 'test-user-id'

        user, user_created = self._authenticate_with_params(params)

        self.assertFalse(user.is_anonymous)
        self.assertTrue(user_created)

    def test_authenticate_with_unknown_user_id_and_create_unknown_off(self):
        params = _get_default_params()
        params['user_id'] = 'test-unkown-user-id-create-unknown-off'

        backend = self._get_backend()
        backend.create_unknown_user = False

        with self.assertRaises(PermissionDenied):
            user, user_created = self._authenticate_with_params(
                params, backend=backend)

    def test_authenticate_with_known_user_id_and_create_unknown_off(self):
        params = _get_default_params()
        params['user_id'] = 'test-kown-user-id-create-unknown-off'

        backend = self._get_backend()
        backend.create_unknown_user = False

        new_user = UserModel.objects.create_user(
            _generate_username_from_valid_params(
                consumer_key, params['user_id']),
        )

        user, user_created = self._authenticate_with_params(
            params, backend=backend)

        self.assertEqual(user, new_user)
        self.assertFalse(user_created)
        self.assertTrue(user.is_authenticated())

    def test_authenicate_for_existing_active_user(self):
        params = _get_default_params()
        params['user_id'] = 'test-existing-active-user'

        new_user = UserModel.objects.create_user(
            _generate_username_from_valid_params(
                consumer_key, params['user_id']),
        )

        user, user_created = self._authenticate_with_params(params)

        self.assertEqual(user, new_user)
        self.assertFalse(user_created)
        self.assertTrue(user.is_authenticated())

    def test_authenicate_for_existing_inactive_user(self):
        params = _get_default_params()
        params['user_id'] = 'test-existing-inactive-user'

        UserModel.objects.create_user(
            _generate_username_from_valid_params(
                consumer_key, params['user_id']),
            is_active=False,
        )

        user, user_created = self._authenticate_with_params(params)

        self.assertIsNone(user)
        self.assertFalse(user_created)

    def test_authenicate_with_user_email(self):
        params = _get_default_params()
        params['user_id'] = 'test_email'
        params['lis_person_contact_email_primary'] = 'foo@example.com'

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user_created)
        self.assertEqual(user.email,
                         params['lis_person_contact_email_primary'])
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_authenticate_with_user_both_names(self):
        params = _get_default_params()
        params['user_id'] = 'test_both_names'
        params['lis_person_name_given'] = 'Firstname'
        params['lis_person_name_family'] = 'Lastname'

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user_created)
        self.assertEqual(user.email, '')
        self.assertEqual(user.first_name, params['lis_person_name_given'])
        self.assertEqual(user.last_name, params['lis_person_name_family'])

    def test_authenticate_with_user_fullname(self):
        params = _get_default_params()
        params['user_id'] = 'test_fullname'
        params['lis_person_name_full'] = 'Firstname Lastname'

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user_created)
        self.assertEqual(user.email, '')
        self.assertEqual(user.first_name, params['lis_person_name_full'])
        self.assertEqual(user.last_name, '')

    def test_authenticate_with_user_fullname_and_firstname(self):
        params = _get_default_params()
        params['user_id'] = 'test_fullname_and_firstname'
        params['lis_person_name_given'] = 'Firstname'
        params['lis_person_name_full'] = 'Fullname'

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user_created)
        self.assertEqual(user.email, '')
        self.assertEqual(user.first_name, params['lis_person_name_full'])
        self.assertEqual(user.last_name, '')

    def test_authenticate_with_user_fullname_and_lastname(self):
        params = _get_default_params()
        params['user_id'] = 'test_fullname_and_lastname'
        params['lis_person_name_family'] = 'Lastname'
        params['lis_person_name_full'] = 'Fullname'

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user_created)
        self.assertEqual(user.email, '')
        self.assertEqual(user.first_name, params['lis_person_name_full'])
        self.assertEqual(user.last_name, '')

    def test_authenticate_with_user_fullname_and_last_and_first_name(self):
        params = _get_default_params()
        params['user_id'] = 'test_fullname_and_first_and_last_name'
        params['lis_person_name_given'] = 'Firstname'
        params['lis_person_name_family'] = 'Lastname'
        params['lis_person_name_full'] = 'Firstname Lastname Fullname'

        user, user_created = self._authenticate_with_params(params)

        self.assertTrue(user_created)
        self.assertEqual(user.email, '')
        self.assertEqual(user.first_name, params['lis_person_name_given'])
        self.assertEqual(user.last_name, params['lis_person_name_family'])


@override_settings(
    LTI_CONSUMER_SECRETS=lti_consumer_secrets,
)
class LtiRequestValidatorTests(TestCase):
    def _get_validator(self):
        return utils.LtiRequestValidator()

    def test_check_client_key_length(self):
        validator = self._get_validator()
        self.assertFalse(validator.check_client_key('tooshort'))
        self.assertFalse(validator.check_client_key(
            ('toolongabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
        ))
        self.assertTrue(validator.check_client_key(
            ('justrightabcdefghijklmnopqrstuvwxyz')
        ))

    def test_check_client_key_characters(self):
        validator = self._get_validator()
        self.assertTrue(validator.check_client_key(
            ('correctabcdefghijklmnopqrstuvwxyz')
        ))
        self.assertFalse(validator.check_client_key(
            ('wrong--abcdefghijklmnopqrstuvwxy')
        ))
        self.assertFalse(validator.check_client_key(
            ('wrong&abcdefghijklmnopqrstuvwxy')
        ))
        self.assertFalse(validator.check_client_key(
            ('wrong?abcdefghijklmnopqrstuvwxy')
        ))

    def test_check_nonce_length(self):
        validator = self._get_validator()
        self.assertFalse(validator.check_nonce('oooooooo9'),
                         '9-character nonce')
        self.assertTrue(validator.check_nonce('oooooooo10ooooo'),
                        '15-character nonce')
        self.assertTrue(validator.check_nonce('oooooooo10oooooooo20'),
                        '20-character nonce')
        self.assertFalse(validator.check_nonce(
            'toolongabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'),
            '59-character nonce'
        )
        self.assertTrue(validator.check_nonce(
            'justrightabcdefghijklmnopqrstuvwxyz'), '35-character nonce')

    def test_check_nonce_characters(self):
        validator = self._get_validator()
        self.assertTrue(validator.check_nonce(
            ('correctabcdefghijklmnopqrstuvwxyz')
        ))
        self.assertFalse(validator.check_nonce(
            ('wrong--abcdefghijklmnopqrstuvwxy')
        ))
        self.assertFalse(validator.check_nonce(
            ('wrong&abcdefghijklmnopqrstuvwxy')
        ))
        self.assertFalse(validator.check_nonce(
            ('wrong?abcdefghijklmnopqrstuvwxy')
        ))

    def test_enforce_ssl_on(self):
        validator = self._get_validator()

        with override_settings(LTI_ENFORCE_SSL=True):
            self.assertTrue(validator.enforce_ssl)

    def test_enforce_ssl_off(self):
        validator = self._get_validator()

        with override_settings(LTI_ENFORCE_SSL=False):
            self.assertFalse(validator.enforce_ssl)

    # Decorated separately because we need to del the LTI_CONSUMER_SECRETS
    # setting for this method only.
    @override_settings()
    def test_enforce_ssl_not_set(self):
        del settings.LTI_ENFORCE_SSL

        validator = self._get_validator()

        self.assertTrue(validator.enforce_ssl)

    def test_get_client_secret_valid(self):
        validator = self._get_validator()

        self.assertEqual(consumer_secret,
                         validator.get_client_secret(consumer_key, None))

    def test_get_client_secret_invalid(self):
        validator = self._get_validator()

        self.assertIsNone(validator.get_client_secret('invalid', None))

    def test_validate_client_key_valid(self):
        validator = self._get_validator()

        self.assertTrue(validator.validate_client_key(consumer_key, None))

    def test_validate_client_key_invalid(self):
        validator = self._get_validator()

        self.assertFalse(validator.validate_client_key('invalid', None))

    def test_validate_timestamp_and_nonce(self):
        validator = self._get_validator()

        timestamp = int(time.time())

        self.assertTrue(validator.validate_timestamp_and_nonce(
            None, timestamp, None, None))

        self.assertTrue(validator.validate_timestamp_and_nonce(
            None, timestamp - 10, None, None), 'not too old')

        self.assertFalse(validator.validate_timestamp_and_nonce(
            None, timestamp - 610, None, None), 'too far in the past')

        self.assertFalse(validator.validate_timestamp_and_nonce(
            None, timestamp + 610, None, None), 'too far in the future')
