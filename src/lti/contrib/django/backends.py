from __future__ import unicode_literals
import logging
import hashlib

from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .models import NonceHistory
from .utils import LtiRequestValidator

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class LtiBackend(ModelBackend):
    create_unknown_user = True

    def _generate_username(self, lti_launch_request):
        username_field = UserModel._meta.get_field('username')

        def _force_clean(string):
            try:
                return username_field.clean(string, None)
            except ValidationError:
                return hashlib.sha1(string.encode()).hexdigest()

        username_string = '_%s_%s' % (
            _force_clean(lti_launch_request.oauth_consumer_key),
            _force_clean(lti_launch_request.user_id),
        )

        return username_string

    def authenticate(self, request, lti_launch_request):
        validator = LtiRequestValidator()
        if not lti_launch_request.is_valid_request(validator):
            logger.warning(
                ('LTI launch request is invalid (oauth_consumer_key: "%s")' %
                    lti_launch_request.oauth_consumer_key)
            )
            logger.debug(
                ('LTI launch params: %s' % lti_launch_request.to_params()))

            raise PermissionDenied

        NonceHistory.objects.create(
            client_key=lti_launch_request.oauth_consumer_key,
            timestamp=lti_launch_request.oauth_timestamp,
            nonce=lti_launch_request.oauth_nonce)

        logger.debug('user_id: %s' % lti_launch_request.user_id)
        if not lti_launch_request.user_id:
            return AnonymousUser

        username = self._generate_username(lti_launch_request)

        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username,
            })
            if created:
                logger.info('LTI user created (%s)' % username)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                raise PermissionDenied

        if self.user_can_authenticate(user):
            user = self.configure_user(user, lti_launch_request)
            logger.debug('LTI user authenticated (%s)' % username)
            return user
        else:
            print('yo')
            return None

    def configure_user(self, user, launch_request):

        user_was_updated = False
        if launch_request.lis_person_contact_email_primary:
            user.email = launch_request.lis_person_contact_email_primary
            user_was_updated = True

        if (launch_request.lis_person_name_given and
                launch_request.lis_person_name_family):
            user.first_name = launch_request.lis_person_name_given
            user.last_name = launch_request.lis_person_name_family
            user_was_updated = True
        elif launch_request.lis_person_name_full:
            user.first_name = launch_request.lis_person_name_full
            user.last_name = ''
            user_was_updated = True

        if user_was_updated:
            user.save()

        return user
