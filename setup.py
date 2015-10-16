import os
import re
import sys
import codecs
from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

here = os.path.abspath(os.path.dirname(__file__))

def read(path):
    return codecs.open(os.path.join(here, path), 'r', 'utf-8').read()

version_file = read('dce_lti_py/__init__.py')
version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M).group(1)

setup(
    name='dce_lti_py',
    version=version,
    description='A python library for building and/or consuming LTI apps',
    author='Jay Luker',
    author_email='jay_luker@harvard.edu',
    url='https://github.com/harvard-dce/dce_lti_py',
    packages=find_packages(),
    install_requires=['lxml', 'oauthlib', 'requests-oauthlib'],
    license='MIT License',
    keywords='lti',
    zip_safe=True,
    test_suite='tests',
    tests_require=['pytest', 'mock==1.0.1', 'httmock'],
    cmdclass={'test': PyTest}
)
