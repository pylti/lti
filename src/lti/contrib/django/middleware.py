import logging
from django.shortcuts import redirect
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from lti.contrib.django import django_tool_provider

logger = logging.getLogger(__name__)


class LtiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not (request.method == 'POST' and request.POST.get('lti_version')):
            # This doesn't look like an LTI launch, continue as usual.
            return self.get_response(request)

        if hasattr(request, 'user') and request.user.is_authenticated:
            # end any existing session
            auth.logout(request)

        launch_request = django_tool_provider.DjangoToolProvider\
            .from_django_request(request=request)

        user = auth.authenticate(request=request,
                                 lti_launch_request=launch_request)

        if user and user.is_anonymous:
            request.user = user
            logger.debug('LTI using AnonymousUser')
        elif user:
            request.user = user
            auth.login(request, user)

            logger.debug('LTI user logged in (%s)' % user.username)

            # stash the launch params into the session for later use
            request.session['lti_launch_params'] = dict(
                launch_request.launch_params)
        else:
            raise PermissionDenied

        return redirect(request.path)
