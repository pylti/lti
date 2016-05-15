====================================
lti: Learning Tools Interoperability
====================================

.. image:: https://travis-ci.org/pylti/lti.svg?branch=master
    :target: https://travis-ci.org/pylti/lti

.. image:: https://codecov.io/gh/pylti/lti/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/pylti/lti

``lti`` is a Python library implementing the
Learning Tools Interperability (LTI) standard.
It is based on dce_lti_py_,
which is based on ims_lti_py_.

.. _dce_lti_py: https://github.com/harvard-dce/dce_lti_py
.. _ims_lti_py: https://github.com/tophatmonocle/ims_lti_py


Installation
============

.. code-block:: sh

    pip install lti


Dependencies
============

* lxml_
* oauthlib_
* requests-oauthlib_

.. _lxml: https://github.com/lxml/lxml
.. _oauthlib: https://github.com/idan/oauthlib
.. _requests-oauthlib: https://github.com/requests/requests-oauthlib


Usage
=====

The primary goal of this library is to provide classes
for building Python LTI tool providers (LTI apps).
To that end, the functionality that you're looking for
is probably in the ``ToolConfig`` and ``ToolProvider`` classes.


Tool Config Example (Django)
----------------------------

Here's an example of a Django view you might use as the
configuration URL when registering your app with the LTI consumer.

.. code-block:: python

    from lti import ToolConfig
    from django.http import HttpResponse


    def tool_config(request):

        # basic stuff
        app_title = 'My App'
        app_description = 'An example LTI App'
        launch_view_name = 'lti_launch'
        launch_url = request.build_absolute_uri(reverse('lti_launch'))

        # maybe you've got some extensions
        extensions = {
            'my_extensions_provider': {
                # extension settings...
            }
        }

        lti_tool_config = ToolConfig(
            title=app_title,
            launch_url=launch_url,
            secure_launch_url=launch_url,
            extensions=extensions,
            description = app_description
        )

        return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')


Tool Provider OAuth Request Validation Example (Django)
-------------------------------------------------------

.. code-block:: python

    from lti.contrib.django import DjangoToolProvider
    from my_app import RequestValidator


    # create the tool provider instance
    secret = 'my LTI app oauth secret'
    tool_provider = DjangoToolProvider.from_django_request(secret, request)

    # the tool provider uses the 'oauthlib' library which requires an instance
    # of a validator class when doing the oauth request signature checking.
    # see https://oauthlib.readthedocs.org/en/latest/oauth1/validator.html for
    # info on how to create one
    validator = RequestValidator()

    # validate the oauth request signature
    ok = tool_provider.is_valid_request(validator)

    # do stuff if ok / not ok


Testing
=======

Unit tests can be run by executing

.. code-block:: sh

    tox

This uses tox_ to set up and run the test environment.

.. _tox: https://tox.readthedocs.org/
