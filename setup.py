from setuptools import setup, find_packages

setup(
    name = 'ims_lti_py',
    version = '0.5',
    description = 'A Python library to help implement IMS LTI tool consumers and providers',
    author = 'Anson MacKeracher',
    author_email = 'anson@tophatmonocle.com',
    url = 'https://github.com/tophatmonocle/ims_lti_py',
    packages = find_packages(),
    install_requires = ['lxml', 'oauth2'],
    license = 'MIT License',
    keywords = 'lti',
    zip_safe = True,
    test_suite = 'tests',
)
