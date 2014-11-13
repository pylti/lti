# ims-lti-py

Python port of the useful [ims-lti](https://github.com/instructure/ims-lti) Ruby library. Makes integrating with LTI pretty easy.

## Status

[![Circle CI](https://circleci.com/gh/tophatmonocle/ims_lti_py/tree/develop.png?style=badge)](https://circleci.com/gh/tophatmonocle/ims_lti_py/tree/develop)

The next version of this library is under development. Tests are failing and PRs are welcome!

## Installation

The easiest way to get the most recent stable build is to grab from the cheeseshop:

```
pip install ims_lti_py
```

Or, if you have setuptools, simply run `python setup.py install` to install the library to your current environment.

## Dependencies

 * [lxml](https://github.com/lxml/lxml)
 * [python-oauth2](https://github.com/simplegeo/python-oauth2)

## Usage

TODO

## Testing
ims-lti-py unit tests can be run with the [nose](http://readthedocs.org/docs/nose/en/latest/) Python library. Once installed, just run

    nosetests tests/
