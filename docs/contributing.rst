Contributing
============

Setup development environment
-----------------------------

If you decide to contribute to code base, you'll first have to fork the project on GitHub, and then clone the project in the local environment. You'll need a GitHub account in order to make a fork.

First make a directory, setup virtualenv, and install dependencies:

.. code-block:: sh

    mkdir pylti
    cd pylti
    pipenv --three
    pipenv install lxml oauthlib requests-oauthlib
    pipenv install tox sphinx --dev

Now that you have setup the development environment, you're ready to clone the project (just replace `<your_github_username>` with your actual GitHub username):

.. code-block:: sh

    git clone https://github.com/<your_github_username>/lti.git lti

For testing, you can build and install library using `setup.py` (but this is not really needed or recommended, as you'll see later):

.. code-block:: sh

    cd lti
    python setyp.py bdist_wheel
    pipenv install dist/lti-0.9.3.whl

or you can let `tox` handle the build process (it will build and execute automated tests):

.. code-block:: sh

    cd lti
    tox

If you want to contribute to documentation, you can build the documentation locally:

.. code-block:: sh

    cd lti/docs
    make html

Now that you have the development environment all setup, it's best to make a new branch for your feature (or bug fix!), and make changes there:

.. code-block:: sh

    git checkout -b my_new_feature

When you finish coding, use `tox` to test the changes. If all is good, push the branch to your fork, and make a pull request.

Keeping your fork synced with upstream
--------------------------------------

If you followed the previously described setup, then you can easily keep your fork up-to-date with the original repository. First, you need to add the upstream repository to your project:

.. code-block:: sh

    git remote add upstream https://github.com/pylti/lti.git

Then, you can fetch the changes made to the master, and then push them to your fork:

.. code-block:: sh

    git fetch upstream
    git merge upstream/master
    git push origin master
