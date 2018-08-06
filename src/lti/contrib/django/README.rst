Install
-------

``pip install lti``

Configure
---------

In your settings.py...

1. Add LTI_CONSUMER_SECRETS dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    LTI_CONSUMER_SECRETS = {
        u'consumer_secret': u'consumer_key',
    }

2. Add middleware
~~~~~~~~~~~~~~~~~

Add ``lti.contrib.django.middleware.LtiMiddleware`` before
``django.middleware.csrf.CsrfViewMiddleware`` to MIDDLEWARE

3. Add backend
~~~~~~~~~~~~~~

Add ``lti.contrib.django.backends.LtiBackend`` to
AUTHENTICATION_BACKENDS

4. [optional] Turn off SSL enforcing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can turn off SSL check by setting LTI\_ENFORCE\_SSL to False.

5. [optional] Specify LTI_CACHE_ALIAS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To store nonces in a cache other than the default,
specify a value for ``LTI_CACHE_ALIAS``.

::

    LTI_CACHE_ALIAS = 'nonces'
