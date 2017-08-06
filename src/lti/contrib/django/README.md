## Install ##

`pip install lti`


## Configure ##

In your settings.py...

### 1. Add LTI\_CONSUMER\_SECRETS dict ###

```
LTI_CONSUMER_SECRETS = {
    u'consumer_secret': u'consumer_key',
}
```

### 2. Add middleware ###

Add `lti.contrib.django.middleware.LtiMiddleware` before `django.middleware.csrf.CsrfViewMiddleware` to MIDDLEWARE

### 3. Add backend ###

Add `lti.contrib.django.backends.LtiBackend` to AUTHENTICATION\_BACKENDS

### 4. [optional] Turn off SSL enforcing ###

You can turn off SSL check by setting LTI\_ENFORCE\_SSL to False.
