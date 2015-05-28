# dce_lti_py

A python library for building and/or consuming LTI apps.

`dce_lti_py` is a fork of [ims_lti_py](https://github.com/tophatmonocle/ims_lti_py).

## Installation

Install via pip:

```
pip install dce_lti_py
```

## Dependencies

 * [lxml](https://github.com/lxml/lxml)
 * [oauthlib](https://github.com/idan/oauthlib)
 * [requests-oauthlib](https://github.com/requests/requests-oauthlib)

## Usage

The primary goal of this library is to provide classes for building python LTI 
tool providers (i.e., LTI apps). To that end, the functionality you're looking
for is probably in the `ToolConfig` and `ToolProvider` classes.

### tool config example (django)

Here's an example of a django view you might use as the configuration URL when
registering your app with the LTI consumer.

```python

    from dce_lti_py import ToolConfig
    from django.http import HttpResponse

    ...
    
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
```

### tool provider oauth request validation example (django)

Here's an example of how you would validate an incoming LTI launch request. You'd
probably do this as part of some auth middleware, e.g., [django-auth-lti](https://github.com/Harvard-University-iCommons/django-auth-lti)

```python

    from dce_lti_py.contrib.django import DjangoToolProvider
    from my_app import RequestValidator
    
    ...
    
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
    ...
```

## Testing
ims-lti-py unit tests can be run by executing

    python setup.py test

Optionally, you can use [tox](https://tox.readthedocs.org/) with the provided `tox.ini` file

## Contributors

* Jay Luker \<<jay_luker@harvard.edu>\> [@lbjay](http://github.com/lbjay), maintainer
* Reinhard Engels \<<reinhard_engels@harvard.edu>\> [@brainheart](https://github.com/brainheart)
