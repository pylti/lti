from __future__ import unicode_literals

from oauthlib.oauth1 import RequestValidator
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.module_loading import import_string

from .models import NonceHistory

import logging
logger = logging.getLogger(__name__)


class LtiConsumerSettingsStorage(object):
    @property
    def _consumers(self):
        if hasattr(settings, 'LTI_CONSUMER_SECRETS'):
            return settings.LTI_CONSUMER_SECRETS
        else:
            return {}

    def get_consumer_secret(self, consumer_key):
        return self._consumers.get(consumer_key)

    def key_exists(self, consumer_key):
        return consumer_key in self._consumers.keys()


def get_lti_consumer_storage():
    if hasattr(settings, 'LTI_CONSUMER_STORAGE'):
        return import_string(settings.LTI_CONSUMER_STORAGE)()
    else:
        return LtiConsumerSettingsStorage()

consumer_storage = get_lti_consumer_storage()


class LtiRequestValidator(RequestValidator):

    @property
    def client_key_length(self):
        return 20, 50

    @property
    def nonce_length(self):
        return 10, 50

    @property
    def enforce_ssl(self):
        if hasattr(settings, 'LTI_ENFORCE_SSL'):
            return bool(settings.LTI_ENFORCE_SSL)
        else:
            return True

    def get_client_secret(self, client_key, request):
        return consumer_storage.get_consumer_secret(client_key)

    def validate_client_key(self, client_key, request):
        return consumer_storage.key_exists(client_key)

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce,
                                     request, request_token=None,
                                     access_token=None):

        window = timedelta(seconds=600)
        ts = datetime.fromtimestamp(int(timestamp))
        now = datetime.now()
        diff = now - ts

        if abs(diff) > window:
            logger.warning('Timestamp too old (age: %s)' % diff)
            return False

        if NonceHistory.objects.filter(client_key=client_key,
                                       timestamp=timestamp,
                                       nonce=nonce).exists():
            logger.warning(
                'Found matching nonce/timestamp, possible replay attack')
            return False

        return True
