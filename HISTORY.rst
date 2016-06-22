0.8.1 (2016-06-22)
++++++++++++++++++

* Python 3 compatibility.

0.8.0 (2016-05-15)
++++++++++++++++++

* Fork from dce_lti_py_, and rename to ``lti`` at version 0.7.4.
* Convert text files to reStructured Text.
* Use README as PyPI long description.

.. _dce_lti_py: https://github.com/harvard-dce/dce_lti_py

0.7.4 (2015-10-16)
++++++++++++++++++

* Include ``oauth_body_hash`` parameter in outcome request.

0.7.3 (2015-05-28)
++++++++++++++++++

* Add some launch params specific to the Canvas editor.
* Add contributor section to README.

0.7.2 (2015-05-01)
++++++++++++++++++

* Use ``find_packages`` in ``setup.py`` to find contrib packages.

0.7.1 (2015-04-30)
++++++++++++++++++

* Fork from _ims_lti_py_, and rename to ``dce_lti_py`` at version 0.6.
* Update README and add HISTORY.

.. _ims_lti_py: https://github.com/tophatmonocle/ims_lti_py

0.7.0 (2015-04-30)
++++++++++++++++++

* Update project to utilize oauthlib.

  * Convert from python-oauth2 to oauthlib and requests-oauthlib.
  * Refactor out the use of mixin classes.
  * Make ``LaunchParams`` a first-class object.
  * Major rewrite and rename of the test suite.
  * Use SemVer version identifier.
  * Use pytest and tox for test running.
