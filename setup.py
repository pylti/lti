from setuptools import setup, find_packages

PKG = 'ims_lti_py'

setup(
    name = PKG,
    version = '0.1',
    description = 'A Ruby library to help implement IMS LTI tool consumers and providers',
    author = 'Anson MacKeracher',
    author_email = 'anson@tophatmonocle.com',
    url = 'https://github.com/tophatmonocle/ims-lti-py',
    packages = find_packages(),
    install_requires = ['lxml', 'oauth2'],
    license = 'MIT License',
    keywords = 'lti',
    zip_save = True,
    test_suite = 'tests'
)
