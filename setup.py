"""Set up the lti package."""
from setuptools import setup, find_packages

setup(
    name='lti',
    version='0.8.0',
    description='A python library for building and/or consuming LTI apps',
    author='Jay Luker',
    author_email='jay_luker@harvard.edu',
    url='https://github.com/pylti/lti',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'lxml',
        'oauthlib',
        'requests-oauthlib',
    ],
    license='MIT License',
    keywords='lti',
    zip_safe=True,
)
