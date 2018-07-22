Getting Started
===============

`lti` is a Python library implementing the Learning Tools Interperability (LTI) standard. It is based on dce_lti_py_, which is based on ims_lti_py_.

.. _dce_lti_py: https://github.com/harvard-dce/dce_lti_py
.. _ims_lti_py: https://github.com/tophatmonocle/ims_lti_py

Installation
------------

You can install the library using `pip`:

.. code-block:: sh

    pip install lti

Or `pipenv`:

.. code-block:: sh

    pipenv install lti

Usage
-----

The primary goal of this library is to provide classes for building Python LTI tool providers (LTI apps). To that end, the functionality that you're looking for is probably in the `ToolConfig` and `ToolProvider` classes (`ToolConsumer` is available too, if you want to consume LTI Providers).

For more info on how to use these classes, look at the examples_.

.. _examples: ./examples.html

Dependencies
------------

* lxml_
* oauthlib_
* requests-oauthlib_

.. _lxml: https://github.com/lxml/lxml
.. _oauthlib: https://github.com/idan/oauthlib
.. _requests-oauthlib: https://github.com/requests/requests-oauthlib
